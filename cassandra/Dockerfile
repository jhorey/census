FROM ferry/cassandra-client
NAME ferry/census-cassandra

# Everything goes in home dir.
RUN mkdir -p /home/ferry/census

# Install everything
WORKDIR /home/ferry/census
RUN apt-get --yes install python-pip git python-dev
# RUN git clone https://bitbucket.org/jhorey/census
ADD ./src /home/ferry/census
RUN pip install -r requirements.txt

# Clean everything
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*
