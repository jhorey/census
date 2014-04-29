from collections import OrderedDict
from census.cass import Cassandra
from census.hive import Hive
from census.geography import Geography
from census.population import Population
import sys
import os
import os.path


class CLI(object):
    def __init__(self):
        self.geo =Geography()
        self.pop =Population()
        self.data_dir = '/tmp/'
        self.cassandra = Cassandra()
        self.hive = Hive()
        
    def print_help(self):
        s = "usage: census CMD ARG\n"
        s += "commands:\n"
        s += "    download (pop|econ) STATE\n"
        s += "    upload (cassandra|hive) STATE\n"
        print s

    def _pretty_row(self, column_names, row_data, replace = {}):
        row = [0] * len(column_names)
        for k in row_data.keys():
            if row_data[k] in replace:
                data = replace[row_data[k]]
            else:
                data = row_data[k]

            if k == 'state':
                state_name = self.geo.codes[k][data]
                row[column_names.index(k)] = "\'" + state_name + "\'"
                row[column_names.index('state_cd')] = data
            elif k == 'county':
                county_name = self.geo.codes[k][state_name][data]
                row[column_names.index(k)] = "\'" + county_name + "\'"
                row[column_names.index('county_cd')] = data
            else:
                row[column_names.index(k)] = data
        return row

    def raw_print(self, output_file, data, header, print_header=False, replace = {}):
        f = open(output_file, 'w')
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

    def _download_geo(self):
        if len(self.geo.states) == 0:
            self.geo.download_states(os.path.join(self.data_dir, "state_codes"))
        if len(self.geo.counties) == 0:
            self.geo.download_counties(os.path.join(self.data_dir, "county_codes"))
        if len(self.geo.zips) == 0:
            self.geo.download_zip(os.path.join(self.data_dir, "zip_codes"))

    def _download_pop(self, state):
        self._download_geo()
        self.pop.geo = self.geo
        output_file = os.path.join(self.data_dir, "%s_pop.psv" % state)
        d = self.pop.query( { 'source' : 'census',
                              'data' : [self.pop.get.cmds['population']['total'],
                                        self.pop.get.cmds['population']['white'],
                                        self.pop.get.cmds['population']['black'],
                                        self.pop.get.cmds['population']['native'],
                                        self.pop.get.cmds['population']['asian'],
                                        self.pop.get.cmds['population']['pacific'],
                                        self.pop.get.cmds['population']['latino']],
                              'year' : 2010},
                            {'state' : state,
                             'county' : '*' } )
        self.raw_print(output_file, d, ['total', 'white', 'black', 'native', 'asian', 'pacific', 'latino', 'state', 'county'])

    def _download_econ(self, state):
        self._download_geo()
        self.pop.geo = self.geo
        output_file = os.path.join(self.data_dir, "%s_econ.psv" % state)
        d = self.pop.query( { 'source' : 'acs',
                         'data' : [self.pop.get.cmds['median'],
                                   self.pop.get.cmds['mean'],
                                   self.pop.get.cmds['capita']],
                         'year' : 2012},
                       {'state' : state,
                        'county' : '*'} )
        self.raw_print(output_file, d, ['median', 'mean', 'capita', 'state', 'county'], replace = {'N':0,'-':0})

    def _upload_cassandra(self, state):
        session = self.cassandra._connect()
        if session:
            self.cassandra._create_tables(session)
            self.cassandra._upload_economic(session, os.path.join(self.data_dir, "%s_econ.psv" % state))
            self.cassandra._upload_population(session, os.path.join(self.data_dir, "%s_pop.psv" % state))
            self.cassandra._close(session)

    def _upload_hive(self, state):
        session = self.hive._connect()
        if session:
            self.hive._create_tables(session)
            self.hive._upload_economic(session, os.path.join(self.data_dir, "%s_econ.psv" % state))
            self.hive._upload_population(session, os.path.join(self.data_dir, "%s_pop.psv" % state))
            self.hive._close(session)

    def dispatch(self, cmd, args):
        if cmd == "set":
            self.data_dir = args[0]
        elif cmd == "download":
            if args[0] == "geo":
                self._download_geo()

            if len(args) > 1:
                if args[0] == "pop":
                    self._download_pop(args[1])
                elif args[0] == "econ":
                    self._download_econ(args[1])
            else:
                print "Please supply name of state"
        elif cmd == "upload":
            if len(args) > 1:
                if args[0] == "cassandra":
                    self._upload_cassandra(args[1])
                elif args[0] == "hive":
                    self._upload_hive(args[1])
            else:
                print "Please supply name of state"

def main():
    cli = CLI()
    if not sys.argv or len(sys.argv) < 2:
        cli.print_help()
    else:
        sys.argv.pop(0)
        cmd = sys.argv.pop(0)
        cli.dispatch(cmd, sys.argv)

