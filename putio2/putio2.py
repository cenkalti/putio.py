# -*- coding: utf-8 -*-
"""
A python wrapper for put.io APIv2

https://github.com/putdotio/putio-apiv2-python


Usage:

# TODO write usage

"""

import os
import re
import json
import logging
import requests
import iso8601
from urllib import urlencode
from pdb import set_trace as st

logger = logging.getLogger(__name__)

API_URL             = 'https://put.io/v2'
ACCESS_TOKEN_URL    = 'https://put.io/v2/oauth2/access_token'
AUTHENTICATION_URL  = 'https://put.io/v2/oauth2/authenticate'


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
        
        attributes = {'client': self}
        self.File = type('File', (_File,), attributes)
        #self.Transfer = type('Transfer', (_Transfer,), attributes)
    
    def request(self, path, method='GET', params=None, data=None, files=None, headers=None, raw=False):
        if not params:
            params = {}
        params['oauth_token'] = self.access_token
        
        url = API_URL + path
        logger.debug('url: %s', url)
        
        r = requests.request(method, url, params=params, data=data, files=files, headers=headers, allow_redirects=True)
        logger.debug('response: %s', r)
        
        if raw:
            return r
        
        logger.debug('content: %s', r.content)
        r = json.loads(r.content)
        
        if r['status'] == 'ERROR':
            raise Exception(r['error_type'])
        
        return r


class _BaseResource(object):
    
    def __init__(self, resource_dict):
        '''Construct the object from a dict'''
        
        self.__dict__.update(resource_dict)
        try:
            self.created_at = iso8601.parse_date(self.created_at)
        except:
            pass
        

class _File(_BaseResource):
    
    def __str__(self):
        return self.name.encode('utf-8')
        
    def __repr__(self):
        # shorten name for display
        name = self.name[:17] + '...' if len(self.name) > 20 else self.name
        return 'File(id=%s, name="%s")' % (self.id, str(self))
        
    @classmethod
    def list(cls, parent_id=0, as_dict=False):
        d = cls.client.request('/files/list', params={'parent_id': parent_id})
        files = d['files']
        files = [cls(f) for f in files]
        if as_dict:
            ids = [f.id for f in files]
            return dict(zip(ids, files))
        return files
    
    @classmethod
    def upload(cls, path, name):
        f = open(path)
        files = {'file': (name, f)}
        d = cls.client.request('/files/upload', method='POST', files=files)
        f.close()
        f = d['file']
        return cls(f)
    
    # @property
    #     def parent(self):
    #         if self.parent_id:
    #             d = self.client.request('/files/%s' % self.parent_id)
    #             f = d['file']
    #             parent = _File(f)
    #             return parent
    
    def dir(self):
        '''Helper function for listing inside of directory'''
        return self.list(parent_id=self.id)
    
    def download(self, dest='.', range=None):
        if range:
            headers = {'Range': 'bytes=%s-%s' % range}
        else:
            headers = None
            
        r = self.client.request('/files/%s/download' % self.id, raw=True, headers=headers)
        
        if range:
            return r.content
            
        filename = re.match('attachment; filename\="(.*)"', r.headers['Content-Disposition']).groups()[0]
        with open(os.path.join(dest, filename), 'wb') as f:
            for data in r.iter_content():
                f.write(data)

    def delete(self):
        return self.client.request('/files/%s/delete' % self.id)
