#!/bin/bash

host="postgres"
port="5432"

# Wait for PostgresSQL DB to be ready
until nc -z "$host" "$port"; do
  echo "Waiting for $host:$port to be ready..."
  sleep 1
done

echo "$host:$port is ready!"

# Init Hive metastore schema
schematool -initSchema -dbType postgres

# Start Hive metastore
hive --service metastore 