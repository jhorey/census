import csv
import logging
import os
import os.path
from string import Template
import sys
from subprocess import Popen, PIPE

PHOME = os.path.dirname(__file__)

class Hive(object):
    def _connect(self):
        # We're using the external 'hive' command to do everything.
        # So there's nothing really to connect.
        return True

    def _close(self, session):
        logging.warning("closing hive")

    def _execute_file(self, data_file):
        cmd = ' hive -f ' + data_file
        output = Popen(cmd, stdout=PIPE, shell=True).stdout.read()
        logging.warning(cmd)
        logging.warning(output.strip())

    def _create_tables(self, session):
        self._execute_file(os.path.join(PHOME, 'scripts/createtable.hql'))

    def _upload_economic(self, session, data_file):
        in_file = open(os.path.join(PHOME, 'scripts/upload.hql'), 'r')
        out_file = open('/tmp/upload.hql', 'w')

        changes = { "FILE":data_file,
                    "TABLE":"economic" }
                    
        for line in in_file:
            s = Template(line).substitute(changes)
            out_file.write(s)

        in_file.close()
        out_file.close()
        self._execute_file('/tmp/upload.hql')

    def _upload_population(self, session, data_file):
        in_file = open(os.path.join(PHOME, 'scripts/upload.hql'), 'r')
        out_file = open('/tmp/upload.hql', 'w')

        changes = { "DIR":"/tmp", 
                    "FILE":data_file ,
                    "TABLE":"population" }
                    
        for line in in_file:
            s = Template(line).substitute(changes)
            out_file.write(s)

        in_file.close()
        out_file.close()
        self._execute_file('/tmp/upload.hql')
