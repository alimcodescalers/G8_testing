from api_testing.grid_apis.grid_api_base import GridAPIBase


class NodesAPI(GridAPIBase):
    def __init__(self):
        super().__init__()

    def get_nodes(self):
        method = 'get'
        api = ['nodes']
        return self.request_api(method=method,
                                api=api)

    def get_nodes_nodeid(self, nodeid):
        method = 'get'
        api = ['nodes', nodeid]
        return self.request_api(api=api,
                                method=method)

