import csv
import logging
import os
import sys
from cassandra import AlreadyExists
from cassandra.cluster import Cluster, NoHostAvailable

class Cassandra(object):

    def _connect(self):
        """
        Connect to the Cassandra cluster and return the session.
        """
        if 'BACKEND_STORAGE_IP' in os.environ:
            host = os.environ['BACKEND_STORAGE_IP']
        else:
            host = 'localhost'

        try:
            cluster = Cluster([host])
            return cluster.connect()
        except NoHostAvailable as e:
            logging.warning(e)
            return None

    def _close(self, session):
        session.shutdown()

    def _create_tables(self, session):
        try:
            query = """
                    CREATE KEYSPACE census
                    WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'}
                    """
            session.execute(query)
        except AlreadyExists:
            pass

        session.set_keyspace("census")
        try:
            query = """
                    CREATE TABLE economic (
                    median INT,
                    mean INT,
                    capita INT,
                    state_name TEXT,
                    state_cd TEXT,
                    county_name TEXT, 
                    county_cd TEXT,
                    PRIMARY KEY(state_name, county_name)
                )
                """
            session.execute(query)
        except AlreadyExists:
            pass

        try:
            query = """
                    CREATE TABLE population (
                    total INT, 
                    white INT, 
                    black INT, 
                    native INT, 
                    asian INT, 
                    pacific INT, 
                    latino INT,
                    state_name TEXT,
                    state_cd TEXT,
                    county_name TEXT,
                    county_cd TEXT,
                    PRIMARY KEY(state_name, county_name)
                    )
                    """
            session.execute(query)
        except AlreadyExists:
            pass

    def _upload_economic(self, session, data_file):
        session.set_keyspace("census")
        f = open(data_file, 'r')
        reader = csv.reader(f, delimiter='|')
        for row in reader:
            median, mean, capita, state, state_cd, county, county_cd = row
            query = """
                    INSERT INTO economic
                    (state_cd, state_name, county_cd, county_name, median, mean, capita)
                    VALUES (%(state_cd)s, %(state_name)s, 
                            %(county_cd)s, %(county_name)s,
                            %(median)s, %(mean)s, %(capita)s) 
                   """
            values = { 'state_cd' : str(state_cd),
                       'state_name' : str(state),
                       'county_cd' : str(county_cd),
                       'county_name' : str(county),
                       'median' : int(median),
                       'mean' : int(mean),
                       'capita' : int(capita) }
            session.execute(query, values)

    def _upload_population(self, session, data_file):
        session.set_keyspace("census")
        f = open(data_file, 'r')
        reader = csv.reader(f, delimiter='|')
        for row in reader:
            total, white, black, native, asian, pacific, latino, state, state_cd, county, county_cd = row
            query = """
                    INSERT INTO population
                    (state_cd, state_name, county_cd, county_name, total, white, black, native, asian, pacific, latino)
                    VALUES (%(state_cd)s, %(state_name)s, 
                            %(county_cd)s, %(county_name)s,
                            %(total)s, %(white)s, %(black)s,
                            %(native)s, %(asian)s, %(pacific)s, %(latino)s) 
                   """
            values = { 'state_cd' : str(state_cd),
                       'state_name' : str(state),
                       'county_cd' : str(county_cd),
                       'county_name' : str(county),
                       'total' : int(total),
                       'white' : int(white),
                       'black' : int(black),
                       'native' : int(native),
                       'asian' : int(asian),
                       'pacific' : int(pacific),
                       'latino' : int(latino) }
            session.execute(query, values)
