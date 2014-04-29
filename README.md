U.S. Census and American Community Survey
=========================================

This is a simple Python library to download, parse, and store data from the U.S. Census and American Community Survey. The library can be run stand-alone but is also designed to work with Cassandra or Hadoop (via Ferry).

Prequisites
-----------

This application is much more interesting if you have [Ferry](http://ferry.opencore.io) installed. Ferry lets you create "big data" clusters on your local machine using high-level commands. That means you can install Hadoop, Cassandra, or OpenMPI without already being an expert in those systems. If you want to try out Ferry, you can grab the [Vagrant](http://www.vagrantup.com) box like this:

```
$ vagrant box add opencore/ferry https://s3.amazonaws.com/opencore/ferry.box
$ vagrant init opencore/ferry
$ vagrant up
```

(If you don't have Vagrant installed, you should probably install that first). At this point, I suggest taking a detour to the Ferry installation page.

Installation
------------

Whether you're using Ferry or not, you'll need to download the library:

```
$ git clone https://github.com/jhorey/census
```

Now if you want to run the library with Hadoop, type:

```
$ cd census
$ ./make.sh hadoop
```

Similarly, if you want to run the library with Cassandra, type:

```
$ cd census
$ ./make.sh cassandra
```

Of course if you really don't want to use Ferry and would rather install the package locally, type:

```
$ cd census
$ sudo python setup.py install
```

Now time to actually populate our database!

U.S. Census API
---------------

First you'll need an API key from the U.S. Census. You can request one [here](http://www.census.gov/developers/tos/key_request.html). If you're using Ferry for either Hadoop or Cassandra, log into the connector:

```
$ ferry ssh sa-xxyyzz
```

The `sa-xxyyzz` is the unique ID of your Hadoop (or Cassandra) cluster. You should have seen that output from the `./make.sh` command. 

After logging into your connector, place the API key in `~/.censuskey`. Now you can start downloading some data. Here are a sequence of commands to download data and store the data in Hadoop. a

```
$ census download pop Tennessee
$ census download pop Kentucy
$ census download econ Tennessee
$ census download econ Kentucky
$ census upload hive Tennessee
$ census upload hive Kentucky
```

If you chose the Cassandra stack, replace `hive` with `cassandra`. You can see that the `census` command is pretty simple. You can download either `pop` (population) or `econ` (economic) data on a state-by-state basis. 

After uploading the data into Hive, you can invoke `hive` to play around with the dataset. 

```
$ hive -e 'select * from economic;'
```

Similarly, the Cassandra client comes with `cqlsh` which is very similar to a SQL prompt. 

Status
------

* Right now, the package is limited to two datasets. The population data from the U.S. Census (organized by race), and economic data from the American Community Survey (mean, median, and per capita). The datasets are organized at the county level.
* These datasets are currently stored in either Cassandra or Hadoop (accessible via Hive). I'm planning on supporting other backends as they become availabe in Ferry. 

Why?
----

Although storing these particular datasets in either Cassandra or Hadoop seems a bit overkill, it's still useful for the following reasons:

* Educational | the Census and ACS datasets are interesting and you can use the Cassandra backend as part of a web application
* Integration | the datasets can be combined with other datasets (e.g., sales, weather, etc.) in Hadoop as part of a data warehouse