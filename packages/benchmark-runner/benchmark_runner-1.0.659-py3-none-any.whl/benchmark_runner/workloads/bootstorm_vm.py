
import os
import time
from multiprocessing import Process

from benchmark_runner.common.logger.logger_time_stamp import logger_time_stamp, logger
from benchmark_runner.common.elasticsearch.elasticsearch_exceptions import ElasticSearchDataNotUploaded
from benchmark_runner.workloads.workloads_exceptions import MissingVMs
from benchmark_runner.workloads.workloads_operations import WorkloadsOperations
from benchmark_runner.common.oc.oc import VMStatus


class BootstormVM(WorkloadsOperations):
    """
    This class runs bootstorm vm
    """

    def __init__(self):
        super().__init__()
        self._name = ''
        self._workload_name = ''
        self._es_index = ''
        self._kind = ''
        self._status = ''
        self._vm_name = ''
        self._data_dict = {}
        self._bootstorm_start_time = {}
        # calc total run time - save first vm run time
        self._bootstorm_first_run_time = None

    def save_error_logs(self):
        """
        This method uploads logs into elastic and s3 bucket in case of error
        @return:
        """
        if self._es_host:
            self._data_dict['run_artifacts_url'] = os.path.join(self._run_artifacts_url,
                                                                f'{self._get_run_artifacts_hierarchy(workload_name=self._get_workload_file_name(self._workload_name), is_file=True)}.tar.gz')
            self._upload_to_elasticsearch(index=self._es_index, kind=self._kind, status='failed',
                                          result=self._data_dict)
            # verify that data upload to elastic search according to unique uuid
            self._verify_elasticsearch_data_uploaded(index=self._es_index, uuid=self._uuid)

    @logger_time_stamp
    def _set_bootstorm_vm_first_run_time(self):
        """
        This method sets the first vm run time
        @return:
        """
        self._bootstorm_first_run_time = time.time()

    @logger_time_stamp
    def _get_bootstorm_vm_total_run_time(self):
        """
        This method retrieves the total run time from the first VM execution
        @return: The delta time from the first VM execution
        """
        delta = time.time() - self._bootstorm_first_run_time
        return round(delta, 3) * self.MILLISECONDS

    @logger_time_stamp
    def _set_bootstorm_vm_start_time(self, vm_name: str = ''):
        """
        This method captures boot start time for specified VM
        @return:
        """
        self._bootstorm_start_time[vm_name] = time.time()

    @logger_time_stamp
    def _ssh_vm(self, vm_name: str):
            """
            Verify ssh into VM and return vm node in success or False if failed
            @return:
            """
            self._virtctl.expose_vm(vm_name=vm_name)
            # wait till vm ssh login
            if self._oc.get_vm_node(vm_name=vm_name):
                vm_node = self._oc.get_vm_node(vm_name=vm_name)
                if vm_node:
                    node_ip = self._oc.get_nodes_addresses()[vm_node]
                    vm_node_port = self._oc.get_exposed_vm_port(vm_name=vm_name)
                    if self._oc.wait_for_vm_ssh(vm_name=vm_name, node_ip=node_ip, vm_node_port=vm_node_port):
                        logger.info(f"Successfully ssh into VM: '{vm_name}' in Node: '{vm_node}' ")
                    return vm_node
            return False

    @logger_time_stamp
    def _get_bootstorm_vm_elapsed_time(self, vm_name: str, vm_node: str) -> dict:
        """
        Returns the boot elapse time for the specified VM in milliseconds.
        @return: Dictionary with vm_name, node, and boot elapse time.
        """
        if vm_node:
            delta = round((time.time() - self._bootstorm_start_time[vm_name]) * self.MILLISECONDS, 3)
            return {'vm_name': vm_name, 'node': vm_node, 'bootstorm_time': delta, 'vm_ssh': int(bool(vm_node)),}
        return {}

    def _create_vm_scale(self, vm_num: str):
        """
        This method creates VMs in parallel
        """
        try:
            self._oc.create_async(yaml=os.path.join(f'{self._run_artifacts_path}', f'{self._name}_{vm_num}.yaml'))
            self._oc.wait_for_vm_status(vm_name=f'{self._workload_name}-{self._trunc_uuid}-{vm_num}', status=VMStatus.Stopped)
        except Exception as err:
            # save run artifacts logs
            self.save_error_logs()
            raise err

    def _finalize_vm(self):
        self._status = 'complete' if self._data_dict else 'failed'
        # prometheus queries
        self._prometheus_metrics_operation.finalize_prometheus()
        metric_results = self._prometheus_metrics_operation.run_prometheus_queries()
        prometheus_result = self._prometheus_metrics_operation.parse_prometheus_metrics(data=metric_results)
        # update total vm run time
        if not self._verification_only:
            total_run_time = self._get_bootstorm_vm_total_run_time()
            self._data_dict.update({'total_run_time': total_run_time})
        self._data_dict.update(prometheus_result)
        if self._es_host:
            # upload several run results
            self._upload_to_elasticsearch(index=self._es_index, kind=self._kind, status=self._status,
                                          result=self._data_dict)
            # verify that data upload to elastic search according to unique uuid
            self._verify_elasticsearch_data_uploaded(index=self._es_index, uuid=self._uuid)

    def _run_vm(self):
        """
        This method runs one VM, upload results to Elasticsearch, and destroys VM synchronously
        @return:
        """
        self._oc.create_async(yaml=os.path.join(f'{self._run_artifacts_path}', f'{self._name}.yaml'))
        self._oc.wait_for_vm_status(vm_name=f'{self._workload_name}-{self._trunc_uuid}', status=VMStatus.Stopped)
        self._set_bootstorm_vm_first_run_time()
        self._set_bootstorm_vm_start_time(vm_name=self._vm_name)
        self._virtctl.start_vm_sync(vm_name=self._vm_name)
        self.vm_node = self._ssh_vm(vm_name=self._vm_name)
        self._data_dict = self._get_bootstorm_vm_elapsed_time(vm_name=self._vm_name, vm_node=self.vm_node)
        self._data_dict['run_artifacts_url'] = os.path.join(self._run_artifacts_url,
                                                            f'{self._get_run_artifacts_hierarchy(workload_name=self._workload_name, is_file=True)}-{self._time_stamp_format}.tar.gz')
        self._finalize_vm()
        self._oc.delete_vm_sync(
            yaml=os.path.join(f'{self._run_artifacts_path}', f'{self._name}.yaml'),
            vm_name=self._vm_name)

    def _verify_vm_ssh(self):
        """
        This method verifies each VM ssh login
        :return:
        """
        try:
            vm_names = self._oc._get_all_vm_names()
            if not vm_names:
                raise MissingVMs
            for vm_name in vm_names:
                vm_node = self._ssh_vm(vm_name)
                self._data_dict = {
                    'vm_name': vm_name,
                    'node': vm_node,
                    'vm_ssh': int(bool(vm_node)),
                    'run_artifacts_url': os.path.join(
                        self._run_artifacts_url,
                        f"{self._get_run_artifacts_hierarchy(workload_name=self._workload_name, is_file=True)}-{self._time_stamp_format}.tar.gz"
                    )
                }
                self._finalize_vm()
        except Exception as err:
            # save run artifacts logs
            self.save_error_logs()
            raise err

    def _run_vm_scale(self, vm_num: str):
        """
        This method runs VMs in parallel and wait for login to be enabled
        """
        try:
            vm_name = f'{self._workload_name}-{self._trunc_uuid}-{vm_num}'
            self._set_bootstorm_vm_start_time(vm_name=f'{self._workload_name}-{self._trunc_uuid}-{vm_num}')
            self._virtctl.start_vm_async(vm_name=f'{self._workload_name}-{self._trunc_uuid}-{vm_num}')
            self._virtctl.wait_for_vm_status(vm_name=vm_name, status=VMStatus.Running)
            vm_node = self._ssh_vm(vm_name)
            self._data_dict = self._get_bootstorm_vm_elapsed_time(vm_name=vm_name, vm_node=vm_node)
            self._data_dict['run_artifacts_url'] = os.path.join(self._run_artifacts_url, f'{self._get_run_artifacts_hierarchy(workload_name=self._workload_name, is_file=True)}-scale-{self._time_stamp_format}.tar.gz')
            self._finalize_vm()
        except Exception as err:
            # save run artifacts logs
            self.save_error_logs()
            raise err

    def _stop_vm_scale(self, vm_num: str):
        """
        This method stops VMs async in parallel
        """
        try:
            self._virtctl.stop_vm_async(vm_name=f'{self._workload_name}-{self._trunc_uuid}-{vm_num}')
        except Exception as err:
            # save run artifacts logs
            self.save_error_logs()
            raise err

    def _wait_for_stop_vm_scale(self, vm_num: str):
        """
        This method waits for VMs stop in parallel
        """
        try:
            self._virtctl.wait_for_vm_status(vm_name=f'{self._workload_name}-{self._trunc_uuid}-{vm_num}')
        except Exception as err:
            # save run artifacts logs
            self.save_error_logs()
            raise err

    def _delete_vm_scale(self, vm_num: str):
        """
        This method deletes VMs async in parallel
        """
        try:
            self._oc.delete_async(
                yaml=os.path.join(f'{self._run_artifacts_path}', f'{self._name}_{vm_num}.yaml'))
        except Exception as err:
            # save run artifacts logs
            self.save_error_logs()
            raise err

    def _wait_for_delete_vm_scale(self, vm_num: str):
        """
        This method waits for VMs delete in parallel
        """
        try:
            self._oc.wait_for_vm_delete(vm_name=f'{self._workload_name}-{self._trunc_uuid}-{vm_num}')
        except Exception as err:
            # save run artifacts logs
            self.save_error_logs()
            raise err

    def _initialize_run(self):
        """
        Initialize prometheus start time, vm name, kind and create benchmark-runner namespace for bootstorm vms
        """
        self._prometheus_metrics_operation.init_prometheus()
        self._name = self._workload
        self._workload_name = self._workload.replace('_', '-')
        self._vm_name = f'{self._workload_name}-{self._trunc_uuid}'
        self._kind = 'vm'
        self._environment_variables_dict['kind'] = 'vm'
        if not self._verification_only:
            # create namespace
            self._oc.create_async(yaml=os.path.join(f'{self._run_artifacts_path}', 'namespace.yaml'))

    def run_vm_workload(self):
        # verification only w/o running or deleting any resource
        if self._verification_only:
            self._verify_vm_ssh()
        else:
            if not self._scale:
                self._run_vm()
            # scale
            else:
                first_run_time_updated = False
                # Run VMs only
                if not self._delete_all:
                    steps = (self._create_vm_scale, self._run_vm_scale)
                else:
                    steps = (self._create_vm_scale, self._run_vm_scale, self._stop_vm_scale,
                             self._wait_for_stop_vm_scale,self._delete_vm_scale, self._wait_for_delete_vm_scale)

                # create run bulks
                bulks = tuple(self.split_run_bulks(iterable=range(self._scale * len(self._scale_node_list)),
                                                   limit=self._threads_limit))
                # create, run and delete vms
                for target in steps:
                    proc = []
                    for bulk in bulks:
                        for vm_num in bulk:
                            # save the first run vm time
                            if self._run_vm_scale == target and not first_run_time_updated:
                                self._set_bootstorm_vm_first_run_time()
                                first_run_time_updated = True
                            p = Process(target=target, args=(str(vm_num),))
                            p.start()
                            proc.append(p)
                        for p in proc:
                            p.join()
                        # sleep between bulks
                        time.sleep(self._bulk_sleep_time)
                        proc = []

    @logger_time_stamp
    def run(self):
        """
        This method runs the workload
        :return:
        """
        try:
            self._initialize_run()
            if self._run_type == 'test_ci':
                self._es_index = 'bootstorm-test-ci-results'
            else:
                self._es_index = 'bootstorm-results'
            self.run_vm_workload()
            # delete namespace
            self._oc.delete_async(yaml=os.path.join(f'{self._run_artifacts_path}', 'namespace.yaml'))
        except ElasticSearchDataNotUploaded as err:
            self._oc.delete_vm_sync(
                yaml=os.path.join(f'{self._run_artifacts_path}', f'{self._name}.yaml'),
                vm_name=self._vm_name)
            raise err
        except Exception as err:
            # save run artifacts logs
            self.save_error_logs()
            raise err
