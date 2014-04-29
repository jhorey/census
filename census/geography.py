from census.get import Get
import json
import os
import sys
import requests
from requests.exceptions import ConnectionError

class Geography(object):
    def __init__(self):
        self.get = Get()
        self.area = {
            'state' : 'state',
            'county' : 'county', 
            'zip' : 'zip+code+tabulation+area'
            }

        self.states = {}
        self.counties = {}
        self.zips = {}
        self.data = {
            'state' : self.states,
            'county' : self.counties,
            'zip' : self.zips
            }
        self.codes = {
            'state' : None,
            'county' : None
            }

    def download_states(self, output_file):
        if not os.path.exists(output_file):
            year = 2010
            url = self.get.api_url + '/' + str(year) + '/' + self.get.surveys['census']
            payload = { 'for' : 'state:*',
                        'get': 'NAME',
                        'key' : self.get.key }
            full = url + '?' + self.get._create_params(payload)
            try:
                res = requests.get(full)
                if res.status_code == 200:
                    f = open(output_file, "w")
                    f.write(res.text)
                    f.close()
            except ConnectionError as e:
                print e.explanation

        self._load_state_codes(output_file)

    def download_counties(self, output_file):
        year = 2010
        url = self.get.api_url + '/' + str(year) + '/' + self.get.surveys['census']
        for s in self.states.keys():
            state_file = output_file + '-' + s
            if not os.path.exists(state_file):
                payload = { 'for' : 'county:*',
                            'in' : 'state:%s' % self.states[s], 
                            'get': 'NAME',
                            'key' : self.get.key }
                full = url + '?' + self.get._create_params(payload)
                try:
                    res = requests.get(full)
                    if res.status_code == 200:
                        f = open(state_file, "w")
                        f.write(res.text.encode('utf8'))
                        f.close()
                except ConnectionError as e:
                    print e.explanation
        self._load_county_codes(output_file)

    def download_zip(self, output_file):
        year = 2010
        url = self.get.api_url + '/' + str(year) + '/' + self.get.surveys['census']

        for s in self.states.keys():
            state_file = output_file + '-' + s
            if not os.path.exists(state_file):
                payload = { 'for' : self.area['zip'] + ':*',
                            'in' : 'state:%s' % self.states[s], 
                            'get': 'NAME',
                            'key' : self.get.key }
                full = url + '?' + self.get._create_params(payload)
                try:
                    res = requests.get(full)
                    if res.status_code == 200:
                        f = open(state_file, "w")
                        f.write(res.text.encode('utf8'))
                        f.close()
                except ConnectionError as e:
                    print e.explanation
        self._load_zip_codes(output_file)

    def _load_state_codes(self, input_file):
        f = open(input_file, "r")
        out = f.read()
        data =  json.loads(out)
        for i, d in enumerate(data):
            if i > 0:
                self.states[d[0]] = d[1]

        # Also create a reverse index
        self.state_codes = {v:k for k, v in self.states.items()}
        self.codes['state'] = self.state_codes

    def _load_county_codes(self, input_file):
        self.county_codes = {}
        for s in self.states.keys():
            state_file = input_file + '-' + s
            f = open(state_file, "r")
            out = f.read()
            data = json.loads(out)

            self.counties[s] = []
            self.county_codes[s] = {}
            for i, d in enumerate(data):
                if i > 0:
                    cd = str(int(d[2]))
                    self.counties[s].append( { d[0] : cd } )
                    self.county_codes[s][cd] = d[0]

        self.codes['county'] = self.county_codes
                    
    def _load_zip_codes(self, input_file):
        for s in self.states.keys():
            state_file = input_file + '-' + s
            f = open(state_file, "r")
            out = f.read()
            data = json.loads(out)

            self.zips[s] = []
            for i, d in enumerate(data):
                if i > 0:
                    self.zips[s].append( d[2] )
