# Docker Hadoop Cluster

This directory contains a simple setup to run a Hadoop cluster using Docker and Docker Compose.

## Requirements
- Docker
- Docker Compose

## How to Start the Cluster
From the `docker_cluster` directory, run:

```sh
docker-compose up -d --build
```

or

```sh
make build-cluster
make start-cluster
```

## How to Stop the Cluster

```sh
docker-compose down
```
or

```sh
make stop-cluster
```



## Containers
The following containers are built and run as part of the cluster:
- **base**: The base Hadoop image.
- **namenode**: Hadoop NameNode (ports: 9870, 9000)
- **datanode**: Hadoop DataNode (port: 9864)
- **resourcemanager**: YARN ResourceManager (port: 8088)
- **nodemanager**: YARN NodeManager (port: 8042)
- **historyserver**: Hadoop HistoryServer (port: 8188)
- **postgres**: PostgreSQL database for Hive Metastore (port: 5432)
- **hivemetastore**: Hive Metastore service (port: 9083)
- **hiveserver**: HiveServer2 (ports: 10000, 10002)

## Build architecture
Each service (except `postgres`) is built from a Dockerfile in its respective subdirectory (e.g., `namenode/`, `datanode/`, etc.). The `docker-compose.yml` file orchestrates the build and startup.

## Web interfaces
You can access the following web UIs from your host machine:
- **Hadoop NameNode UI**: http://localhost:9870
- **Hadoop DataNode UI**: http://localhost:9864
- **YARN ResourceManager UI**: http://localhost:8088
- **YARN NodeManager UI**: http://localhost:8042
- **HistoryServer UI**: http://localhost:8188
- **HiveServer2**: http://localhost:10002

