#!/bin/bash

# Hive variables
export HIVE_HOME=/opt/hive
export HIVE_CONF_DIR=$HIVE_HOME/conf
export PATH=$PATH:$HIVE_HOME/bin
export HADOOP_CLASSPATH=$HADOOP_CLASSPATH:$HIVE_HOME/lib/*
export HADOOP_OPTS="$HADOOP_OPTS -Djava.net.preferIPv4Stack=true"

# Hive metastore variables
export HIVE_METASTORE_HADOOP_VERSION=3.3.6
export HIVE_METASTORE_PORT=9083
export HIVE_METASTORE_URI=thrift://hivemetastore:9083

# Hive Server2 variables
export HIVE_SERVER2_THRIFT_PORT=10000
export HIVE_SERVER2_WEBUI_PORT=10002 

# PostgreSQL variables
export POSTGRES_HOST=postgres
export POSTGRES_USER=hive
export POSTGRES_PASSWORD=hive
export POSTGRES_DB=metastore