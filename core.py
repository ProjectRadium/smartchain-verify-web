#/usr/bin/env python
# -*- coding: utf-8 -*-
import requests, datetime, validators, ast, urllib2
from hashlib import sha256
from urlparse import urlparse

class core():
    def __init__(self):
        self.api_url = "http://smartchainapi.azurewebsites.net/?"
        # File size limit: 50 MB
        self.file_size_limit = 50000000
        # Error codes
        self.codes = ['File successfully verified by a verified user.', 'File successfully verified by an unverified user.', 'File not verified.', 'URL is invalid.', 'File is above the maximum file size.']

    def get_domain(self, url):
        return '{uri.netloc}'.format(uri=urlparse(url))

    def get_api_data(self, ext, data):
        return requests.get("%s%s=%s" % (self.api_url, ext, data)).content

    def is_valid_url(self, url):
        if validators.url(url):
            return True
        else:
            if url[:8] == "https://":
                if validators.url("http://%s" % (url[8:])):
                    return True
                else:
                    return False
            else:
                if validators.url("http://%s" % (url)):
                    return [True, "http://"]

    def get_utc_from_unix(self, utime):
        return datetime.datetime.utcfromtimestamp(utime).strftime('%Y-%m-%d %H:%M:%S')

    def get_file_headers(self, url):
        return requests.head(url).headers

    def is_file_under_limit(self, url):
        if url[:8] == 'https://':
            req = urllib2.Request(url, headers={'User-Agent': 'Magic Browser'})
            con = urllib2.urlopen(req)
            if int(con.info().getheaders("Content-Length")[0]) <= self.file_size_limit:
                return True
            else:
                return False
        else:
            file_headers = self.get_file_headers(url)
            for s in file_headers:
                    if s == 'Content-Length':
                        if int(file_headers[s]) <= self.file_size_limit:
                            return True
            else:
                return False

    def get_file_contents(self, url):
        return requests.get(url).content

    def get_file_hash(self, url):
        return sha256(self.get_file_contents(url)).hexdigest()

    def is_hash_acct_verified(self, fhash):
        data = ast.literal_eval(self.get_api_data("hash", fhash))
        is_error = data['error']
        if is_error == 'false': # If there is no error we continue to check if the hash is verified
            is_verified = data['result']['verified']
            if is_verified == 'true': # If is_verified then we can look for the address
                address = data['result']['address']
                address_data =  ast.literal_eval(self.get_api_data("address", address))
                if address_data['verified'] == 'True':
                    return True
                else:
                    return False
            else:
                return False

    def process_data(self, url):
        is_valid_url = self.is_valid_url(url)
        if is_valid_url == [True, 'http://']:
            url = "http://%s" % (url)
        is_valid_url = self.is_valid_url(url)
        if is_valid_url:
            if self.is_file_under_limit(url):
                fhash = self.get_file_hash(url)
                api_data = ast.literal_eval(self.get_api_data("hash", fhash))
                api_data_error = api_data['error']
                if api_data_error == 'false':
                    api_data = api_data['result']
                    if api_data['verified'] == 'true':
                        if self.is_hash_acct_verified(fhash):
                            return {
                                'code':0,
                                'error':False,
                                'message':self.codes[0],
                                'data':{
                                    'verified':True,
                                    'username':api_data['username'],
                                    'user_verified':True,
                                    'title':api_data['title'],
                                    'timestamp':api_data['linuxtime'],
                                    'timestamp_utc':self.get_utc_from_unix(api_data['linuxtime']),
                                    'block':api_data['block']
                                }
                            }
                        else:
                            return {
                                'code': 1,
                                'error': False,
                                'message': self.codes[1],
                                'data': {
                                    'verified': True,
                                    'username': api_data['username'],
                                    'user_verified': False,
                                    'title': api_data['title'],
                                    'timestamp': api_data['linuxtime'],
                                    'timestamp_utc': self.get_utc_from_unix(api_data['linuxtime']),
                                    'block': api_data['block']
                                }
                            }
                    else:
                        return {
                            'code':2,
                            'error':True,
                            'message':self.codes[2]
                        }
                else:
                    return {
                        'code':2,
                        'error':True,
                        'message':self.codes[2]
                    }
            else:
                return {
                    'code':4,
                    'error':True,
                    'message':self.codes[4]
                }
        else:
            return {
                'code':3,
                'error':True,
                'message':self.codes[3]
            }

    def code_lookup(self, code):
        if code > 4:
            return "Invalid code."
        else:
            return self.codes[code]
