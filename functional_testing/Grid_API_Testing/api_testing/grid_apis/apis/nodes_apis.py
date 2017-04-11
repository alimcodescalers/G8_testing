from api_testing.grid_apis.grid_api_base import GridAPIBase


class NodesAPI(GridAPIBase):
    def __init__(self):
        super(NodesAPI, self).__init__()

    def get_node(self):
        method = 'get'
        api = ['node']
        return self.request_api(method=method,
                                api=api)

    def get_node_nodeid(self, node_id):
        method = 'get'
        api = ['node', node_id]
        return self.request_api(api=api,
                                method=method)

    def get_running_jobs(self, node_id):
        method = 'get'
        api = ['node', node_id, 'job']
        return self.request_api(api=api,
                                method=method)

    def kill_running_jobs(self, node_id, job_id=''):
        method = 'delete'
        api = ['node', node_id, 'job']
        return self.request_api(api=api,
                                method=method)

    def kill_job(self, node_id, job_id):
        method = 'delete'
        api = ['node', node_id, 'job', job_id]
        return self.request_api(api=api,
                                method=method)


    def get_job_details(self, node_id, job_id=''):
        method = 'get'
        api = ['node', node_id, 'job', job_id]

        return self.request_api(api=api,
                                method=method)

    def ping_node(self, node_id):
        method = 'post'
        api = ['node', node_id, 'ping']

        return self.request_api(api=api,
                                method=method)

    def get_node_state(self, node_id):
        method = 'get'
        api = ['node', node_id, 'state']

        return self.request_api(api=api,
                                method=method)

    def reboot_node(self, node_id):
        method = 'post'
        api = ['node', node_id, 'reboot']

        return self.request_api(api=api,
                                method=method)


    def get_disks_detail(self, node_id):
        method = 'get'
        api = ['node', node_id, 'disk']

        return self.request_api(api=api,
                                method=method)
