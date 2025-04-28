#!/bin/bash

host="hivemetastore"
port="9083"

# Wait for Hive metastore to be ready
until nc -z "$host" "$port"; do
  echo "Waiting for $host:$port to be ready..."
  sleep 1
done

echo "$host:$port is ready!"

# Start HiveServer2
hiveserver2