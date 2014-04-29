import csv
import os
import sys
import hive_utils

class Hive(object):
    def _connect(self):
        """
        Connect to the Hadoop cluster and return the session.
        """
        if 'BACKEND_STORAGE_IP' in os.environ:
            host = os.environ['BACKEND_STORAGE_IP']
        else:
            host = 'localhost'

        session = hive_utils.HiveClient(server=host, 
                                        port=10000,
                                        db='default')
        return session
