FROM ferry/hadoop-client
NAME ferry/census-hadoop

# Everything goes in home dir.
RUN mkdir -p /home/ferry/census

# Install everything
WORKDIR /home/ferry/census
RUN apt-get --yes install python-pip git
RUN git clone https://github.com/opencore/census
RUN pip install -r src/requirements.txt

# Clean everything
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*
