import logging
import os
import os.path

"""
Simple lookup for US Census requests. 
These codes are for the population & housing tables at the block level. 
https://www.census.gov/developers/data/sf1.xml
"""
class Get(object):
    def __init__(self):
        self.api_url = 'http://api.census.gov/data'
        self.surveys = {'census' : 'sf1', 
                        'acs' : 'acs5/profile'}
        self.cmds = {
            'median': 'DP03_0062E',
            'mean': 'DP03_0063E',
            'capita' : 'DP03_0088E',
            'population' : {
                'total' : 'P0010001',
                'white' : 'P0030002',
                'black' : 'P0030003',
                'native' : 'P0030004',
                'asian' : 'P0030005',
                'pacific' : 'P0030006',
                'latino' : 'P0040003'
                }
            }
        self.key = None
        self._fetch_api_key()

    def _fetch_api_key(self):
        key_file = os.path.join(os.environ['HOME'], '.censuskey')
        if os.path.exists(key_file):
            f = open(key_file, 'r')
            self.key = f.read().strip()
            f.close()
        else:
            logging.error("Could not find " + key_file)
            exit(1)

    def _create_params(self, params):
        args = ''
        for i, p in enumerate(params.keys()):
            if isinstance(params[p], list):
                args += "%s=%s" % (p, ','.join(params[p]))
            else:
                args += "%s=%s" % (p, params[p])
            if i < len(params) - 1:
                args += "&"
        return args

