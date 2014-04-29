#! /bin/bash

# Bash colors
GREEN='\e[0;32m'
NC='\e[0m'

function print {
    echo -e "${GREEN} ${1} ${NC}"
}

if [[ $# == 0 ]]; then
    print "usage: make.sh (cassandra|hive)"
    exit 1
fi

if [[ $1 == "cassandra" ]]; then
    print "Creating Cassandra image"
    cd census/cassandra/
    ferry start census.yml -b ./
elif [[ $1 == "hive" ]]; then
    print "Creating Hive image"
    cd census/hive/
    ferry start census.yml -b ./
fi