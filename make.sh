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
    cp cassandra/Dockerfile Dockerfile
    ferry start cassandra/census.yml -b ./
    rm Dockerfile
elif [[ $1 == "hive" ]]; then
    print "Creating Hive image"
    cp hive/Dockerfile Dockerfile
    ferry start hive/census.yml -b ./
    rm Dockerfile
fi