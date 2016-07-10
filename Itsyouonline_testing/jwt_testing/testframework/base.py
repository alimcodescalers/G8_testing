import pycurl
import StringIO
import requests
import subprocess

class Oauth:
    def __init__(self, env_url):
        self.session = requests.Session()
        self.env_url = env_url

    def login_via_client_credentials(self, client_id, client_secret):
        url = self.env_url + 'v1/oauth/jwt'
        params = {'grant_type': 'client_credentials',
                  'client_id': client_id,
                  'client_secret': client_secret}
        data = self.session.post(url, params=params)
        if data.status_code != 200:
            raise RuntimeError("Failed to login")
        token = data.json()['access_token']
        self.session.headers['Authorization'] = 'token {token}'.format(token=token)

    def curl_cmd(*args):
        curl_path = '/usr/bin/curl'
        curl_list = [curl_path]
        for arg in args:
            curl_list.append(arg)
        curl_result = subprocess.Popen(
                     curl_list,
                     stderr=subprocess.PIPE,
                     stdout=subprocess.PIPE).communicate()[0]
        return curl_result

    def curl(self):
        response = StringIO.StringIO()
        c = pycurl.Curl()
        c.setopt(c.URL, self.env_url + 'v1/oauth/jwt')
        c.setopt(c.WRITEFUNCTION, response.write)
        c.setopt(c.HTTPHEADER, ['Content-Type: application/json','Accept-Charset: UTF-8'])
        c.setopt(c.POSTFIELDS, '@request.json')
        c.perform()
        c.close()
        res = response.getvalue()
        response.close()
        return res
