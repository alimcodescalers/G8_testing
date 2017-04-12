from api_testing.grid_apis.grid_api_base import GridAPIBase


class NodesAPI(GridAPIBase):
    def __init__(self):
        super(NodesAPI, self).__init__()

    def get_nodes(self):
        method = 'get'
        api = ['nodes']
        return self.request_api(method=method,
                                api=api)

    def get_nodes_nodeid(self, node_id):
        method = 'get'
        api = ['nodes', node_id]
        return self.request_api(api=api,
                                method=method)

    def get_nodes_nodeid_jobs(self, node_id):
        method = 'get'
        api = ['nodes', node_id, 'jobs']
        return self.request_api(api=api,
                                method=method)

    def delete_nodes_nodeid_jobs(self, node_id):
        method = 'delete'
        api = ['nodes', node_id, 'jobs']
        return self.request_api(api=api,
                                method=method)

    def get_nodes_nodeid_jobs_jobid(self, node_id, job_id):
        method = 'get'
        api = ['nodes', node_id, 'jobs', job_id]

        return self.request_api(api=api,
                                method=method)

    def delete_nodes_nodeid_jobs_jobid(self, node_id, job_id):
        method = 'delete'
        api = ['nodes', node_id, 'jobs', job_id]
        return self.request_api(api=api,
                                method=method)

    def post_nodes_nodeid_ping(self, node_id):
        method = 'post'
        api = ['nodes', node_id, 'ping']

        return self.request_api(api=api,
                                method=method)

    def get_nodes_nodeid_state(self, node_id):
        method = 'get'
        api = ['node', node_id, 'state']

        return self.request_api(api=api,
                                method=method)

    def post_nodes_nodeid_reboot(self, node_id):
        method = 'post'
        api = ['node', node_id, 'reboot']

        return self.request_api(api=api,
                                method=method)

    def get_nodes_nodeid_cpu(self, node_id):
        method = 'post'
        api = ['nodes', node_id, 'cpu']

        return self.request_api(api=api,
                                method=method)

    def get_nodes_nodeid_disk(self, node_id):
        method = 'get'
        api = ['nodes', node_id, 'disk']

        return self.request_api(api=api,
                                method=method)

    def get_nodes_nodeid_mem(self, node_id):
        method = 'get'
        api = ['nodes', node_id, 'mem']

        return self.request_api(api=api,
                                method=method)

    def get_nodes_nodeid_nic(self, node_id):
        method = 'get'
        api = ['nodes', node_id, 'nic']

        return self.request_api(api=api,
                                method=method)

    def get_nodes_nodeid_info(self, node_id):
        method = 'get'
        api = ['nodes', node_id, 'info']

        return self.request_api(api=api,
                                method=method)

    def get_nodes_nodeid_process(self, node_id):
        method = 'get'
        api = ['nodes', node_id, 'process']

        return self.request_api(api=api,
                                method=method)

    def get_nodes_nodeid_process_processid(self, node_id, process_id):
        method = 'get'
        api = ['nodes', node_id, 'process', process_id]

        return self.request_api(api=api,
                                method=method)

    def delete_nodes_nodeid_process_processid(self, node_id, process_id):
        method = 'delete'
        api = ['nodes', node_id, 'process', process_id]

        return self.request_api(api=api,
                                method=method)

    def post_nodes_nodeid_bridges(self, node_id, body):
        method = 'post'
        api = ['nodes', node_id, 'bridges']

        return self.request_api(api=api,
                                method=method, body=body)

    def get_nodes_nodeid_bridges(self, node_id):
        method = 'get'
        api = ['nodes', node_id, 'bridges']

        return self.request_api(api=api,
                                method=method)

    def get_nodes_nodeid_bridges_bridgeid(self, node_id, bridge_id):
        method = 'get'
        api = ['nodes', node_id, 'bridges',bridge_id]

        return self.request_api(api=api,
                                method=metho

    def delete_nodes_nodeid_bridges_bridgeid(self, node_id, bridge_id):
        method = 'delete'
        api = ['nodes', node_id, 'bridges',bridge_id]

        return self.request_api(api=api,
                                method=method)
