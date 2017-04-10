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

