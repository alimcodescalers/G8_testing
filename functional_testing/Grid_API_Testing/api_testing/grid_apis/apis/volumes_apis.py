from api_testing.grid_apis.grid_api_base import GridAPIBase


class VolumesAPIs(GridAPIBase):
    def __init__(self):
        super().__init__()

    def get_volumes(self):
        method = 'get'
        api = ['volumes']
        return self.request_api(method=method,
                                api=api)

    def post_volumes(self, body):
        method = 'post'
        api = ['volumes']
        return self.request_api(method=method,
                                api=api, body=body)

    def get_volumes_volumeid(self, volumeid):
        method = 'get'
        api = ['volumes', volumeid]
        return self.request_api(method=method,
                                api=api)

    def delete_volumes_volumeid(self, volumeid):
        method = 'delete'
        api = ['volumes', volumeid]
        return self.request_api(method=method,
                                api=api)

    def post_volumes_volumeid_resize(self, volumeid, body):
        method = 'post'
        api = ['volumes', volumeid, 'resize']
        return self.request_api(method=method,
                                api=api, body=body)
    def post_volumes_volumeid_rollback(self, volumeid, body):
        method = 'post'
        api = ['volumes', volumeid, 'rollback']
        return self.request_api(method=method,
                                api=api, body=body)
