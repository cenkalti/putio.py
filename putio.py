# -*- coding: utf-8 -*-
import os
import re
import json
import logging
import webbrowser
from urllib import urlencode

import requests
import iso8601

BASE_URL = 'https://api.put.io/v2'
ACCESS_TOKEN_URL = 'https://api.put.io/v2/oauth2/access_token'
AUTHENTICATION_URL = 'https://api.put.io/v2/oauth2/authenticate'

logger = logging.getLogger(__name__)


class AuthHelper(object):

    def __init__(self, client_id, client_secret, redirect_uri, type='code'):
        self.client_id = client_id
        self.client_secret = client_secret
        self.callback_url = redirect_uri
        self.type = type

    @property
    def authentication_url(self):
        """Redirect your users to here to authenticate them."""
        params = {
            'client_id': self.client_id,
            'response_type': self.type,
            'redirect_uri': self.callback_url
        }
        return AUTHENTICATION_URL + "?" + urlencode(params)

    def open_authentication_url(self):
        webbrowser.open(self.authentication_url)
    
    def get_access_token(self, code):
        params = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'authorization_code',
            'redirect_uri': self.callback_url,
            'code': code
        }
        response = requests.get(ACCESS_TOKEN_URL, params=params)
        logger.debug(response)
        assert response.status_code == 200
        return response.json()['access_token']


class Client(object):
    
    def __init__(self, access_token):
        self.access_token = access_token
        self.session = requests.session()

        # Keep resource classes as attributes of client.
        # Pass client to resource classes so resource object
        # can use the client.
        attributes = {'client': self}
        self.File = type('File', (_File,), attributes)
        self.Transfer = type('Transfer', (_Transfer,), attributes)

    def request(self, path, method='GET', params=None, data=None, files=None,
                headers=None, raw=False):
        """
        Wrapper around requests.request()

        Prepends BASE_URL to path.
        Inserts oauth_token to query params.
        Parses response as JSON and returns it.

        """
        if not params:
            params = {}

        if not headers:
            headers = {}

        # All requests must include oauth_token
        params['oauth_token'] = self.access_token

        headers['Accept'] = 'application/json'

        url = BASE_URL + path
        logger.debug('url: %s', url)
        
        response = self.session.request(
            method, url, params=params, data=data, files=files,
            headers=headers, allow_redirects=True)
        logger.debug('response: %s', response)
        if raw:
            return response
        
        logger.debug('content: %s', response.content)
        try:
            response = json.loads(response.content)
        except ValueError:            
            raise Exception('Server didn\'t send valid JSON:\n%s\n%s' % (
                response, response.content))

        if response['status'] == 'ERROR':
            raise Exception(response['error_type'])
        
        return response


class _BaseResource(object):

    client = None
    
    def __init__(self, resource_dict):
        """Constructs the object from a dict."""
        # All resources must have id and name attributes
        self.id = None
        self.name = None
        self.__dict__.update(resource_dict)
        try:
            self.created_at = iso8601.parse_date(self.created_at)
        except iso8601.ParseError:
            pass
    
    def __str__(self):
        return self.name.encode('utf-8')

    def __repr__(self):
        # shorten name for display
        name = self.name[:17] + '...' if len(self.name) > 20 else self.name
        return '<%s id=%r, name="%r">' % (
            self.__class__.__name__, self.id, name)


class _File(_BaseResource):

    @classmethod
    def get(cls, id):
        d = cls.client.request('/files/%i' % id, method='GET')
        t = d['file']
        return cls(t)

    @classmethod
    def list(cls, parent_id=0):
        d = cls.client.request('/files/list', params={'parent_id': parent_id})
        files = d['files']
        return [cls(f) for f in files]

    @classmethod
    def upload(cls, path, name=None):
        with open(path) as f:
            if name:
                files = {'file': (name, f)}
            else:
                files = {'file': f}
            d = cls.client.request('/files/upload', method='POST', files=files)

        f = d['file']
        return cls(f)

    def dir(self):
        """List the files under directory."""
        return self.list(parent_id=self.id)
    
    def download(self, dest='.'):
        response = self.client.request(
            '/files/%s/download' % self.id, raw=True)

        filename = re.match(
            'attachment; filename="(.*)"',
            response.headers['Content-Disposition']).groups()[0]

        with open(os.path.join(dest, filename), 'wb') as f:
            for data in response.iter_content():
                f.write(data)

    def delete(self):
        return self.client.request('/files/delete', method='POST',
                                   data={'file_ids': str(self.id)})


class _Transfer(_BaseResource):
        
    @classmethod
    def list(cls):
        d = cls.client.request('/transfers/list')
        transfers = d['transfers']
        return [cls(t) for t in transfers]

    @classmethod
    def get(cls, id):
        d = cls.client.request('/transfers/%i' % id, method='GET')
        t = d['transfer']
        return cls(t)

    @classmethod
    def add(cls, url, parent_id=0, extract=False, callback_url=None):
        d = cls.client.request('/transfers/add', method='POST', data=dict(
            url=url, parent_id=parent_id, extract=extract,
            callback_url=callback_url))
        t = d['transfer']
        return cls(t)

    @classmethod
    def add_torrent(cls, path, parent_id=0, extract=False, callback_url=None):
        with open(path) as f:
            files = {'file': f}
            d = cls.client.request('/files/upload', method='POST', files=files,
                                   data=dict(parent_id=parent_id,
                                             extract=extract,
                                             callback_url=callback_url))
        t = d['transfer']
        return cls(t)
