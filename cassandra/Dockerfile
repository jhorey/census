FROM ferry/cassandra-client
NAME ferry/census-cassandra

# Everything goes in home dir.
RUN mkdir -p /home/ferry/census

# Install everything
WORKDIR /home/ferry/census
RUN apt-get --yes install python-pip git
RUN git clone https://bitbucket.org/jhorey/census
RUN pip install -r src/requirements.txt

# Clean everything
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*
