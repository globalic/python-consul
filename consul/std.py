from six.moves import urllib

import requests

from consul import base


__all__ = ['Consul']


class HTTPClient(object):
    def __init__(self, host='127.0.0.1', port=8500, scheme='http',
                 auth=('', ''), verify=True):
        self.host = host
        self.port = port
        self.scheme = scheme
        self.verify = verify
        self.auth = auth
        self.base_uri = '%s://%s:%s' % (self.scheme, self.host, self.port)
        self.session = requests.session()

    def response(self, response):
        return base.Response(
            response.status_code, response.headers, response.text)

    def uri(self, path, params=None):
        uri = self.base_uri + path
        if not params:
            return uri
        return '%s?%s' % (uri, urllib.parse.urlencode(params))

    def get(self, callback, path, params=None):
        uri = self.uri(path, params)
        return callback(self.response(
            self.session.get(uri, verify=self.verify, auth=self.auth)))

    def put(self, callback, path, params=None, data=''):
        uri = self.uri(path, params)
        return callback(self.response(
            self.session.put(uri, data=data, verify=self.verify, auth=self.auth)))

    def delete(self, callback, path, params=None):
        uri = self.uri(path, params)
        return callback(self.response(
            self.session.delete(uri, verify=self.verify, auth=self.auth)))


class Consul(base.Consul):
    def connect(self, host, port, scheme, auth, verify=True):
        return HTTPClient(host, port, scheme, auth, verify)
