FROM ferry/cassandra-client
NAME ferry/census-cassandra

# Install everything
WORKDIR /home/ferry
RUN apt-get --yes install python-pip git python-dev
RUN git clone https://github.com/jhorey/census
WORKDIR /home/ferry/census
RUN python setup.py install

# Clean everything
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*
