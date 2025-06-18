FROM hadoop-base:latest

# Check if the datanode is running
HEALTHCHECK CMD curl -f http://localhost:9864/ || exit 1

RUN mkdir -p /hadoop/dfs/data
VOLUME /hadoop/dfs/data

EXPOSE 9864

CMD ["bash", "-c", "$HADOOP_HOME/bin/hdfs --config $HADOOP_CONF_DIR datanode"]