# -*- coding: utf-8 -*-
"""
A python wrapper for put.io APIv2

https://github.com/putdotio/putio-apiv2-python

"""

import json
import requests
from urllib import urlencode

API_URL = 'https://put.io/v2'
ACCESS_TOKEN_URL = 'https://api.put.io/v2/oauth2/access_token'
AUTHENTICATION_URL = 'https://api.put.io/v2/oauth2/authenticate'


class AuthHelper(object):
    def __init__(self, client_id, client_secret, redirect_uri):
        self.client_id = client_id
        self.client_secret = client_secret
        self.callback_url = redirect_uri
    
    def get_authentication_url(self):
        params = {
            'client_id': self.client_id,
            'response_type': 'code',
            'redirect_uri': self.callback_url
        }
        query_str = urlencode(query)
        return AUTHENTICATION_URL + "?" + query_str
    
    def get_access_token(self, code):
        params = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'authorization_code',
            'redirect_uri': self.callback_url,
            'code': code
        }
        r = requests.get(ACCESS_TOKEN_URL, params=params)
        d = json.loads(r.content)
        return d['access_token']
    
    
class Client(object):
    def __init__(self, access_token):
        self.access_token = access_token
                
    def request(self, method='GET', path, params=None, data=None):
        if not params:
            params = {}
        params['oauth_token'] = self.access_token
        
        url = API_URL + path
        print 'url:', url
        r = requests.request(method, url, params=params, data=data)
        print r; print r.content
        return json.loads(r.content)
    
    def files_list(self, parent_id=0):
        return self.request('/files/list', params=dict(parent_id=parent_id))
    
    def files_download(self, file_id=0):
        return self.request('/files/%s' % file_id)
    
    def files_delete(self, file_id=0):
        return self.request('/files/%s/delete' % file_id)
