from collections import OrderedDict
from census.get import Get
import json
import os
import requests
import sys
from requests.exceptions import ConnectionError

class Population(object):
    def __init__(self):
        self.get = Get()
        self.geo = None
        self.output_file = None

    def raw_print(self, data, header, print_header=False, replace = {}):
        f = open(self.output_file, 'w')
        for i, d in enumerate(data):
            if i == 0:
                data_key = header[0]
                column_names = []
                for h in header:
                    if h == 'state':
                        column_names.append('state')
                        column_names.append('state_cd')
                    elif h == 'county':
                        column_names.append('county')
                        column_names.append('county_cd')
                    else:
                        column_names.append(h)
                if print_header:
                    o = '|'.join(column_names) + '\n'
                    f.write(o)
            elif i > 0:
                row_data = OrderedDict()
                for j, e in enumerate(d):
                    if header[j] == 'county':
                        cd = str(int(e))
                        row_data[header[j]] = cd
                    else:
                        row_data[header[j]] = e
                row = self._pretty_row(column_names, row_data, replace)
                o = '|'.join(row) + '\n'
                f.write(o)
        f.close()

    def query(self, repo, filters):
        url = self.get.api_url + '/' + str(repo['year']) + '/' + self.get.surveys[repo['source']]

        payload = { 'get': repo['data'],
                    'key' : self.get.key }

        if len(filters.keys()) == 1 and 'state' in filters:
                payload['for'] = self.geo.area['state'] + ':' +self.geo.data['state'][filters['state']]
        else:
            for f in filters.keys():
                if f == "state":
                    if filters[f] == '*':
                        loc = '*'
                    else:
                        loc = self.geo.data[f][filters[f]]
                    payload['in'] = self.geo.area['state'] + ':' + loc
                else:
                    if filters[f] == '*':
                        loc = '*'
                    else:
                        loc = self.geo.data[f][filters[f]]
                    payload['for'] = self.geo.area[f] + ':' + loc

        full = url + '?' + self.get._create_params(payload)
        try:
            res = requests.get(full)
            if res.status_code == 200:
                return json.loads(res.text)
            else:
                print full
                print res.text
        except ConnectionError as e:
            print e.explanation

