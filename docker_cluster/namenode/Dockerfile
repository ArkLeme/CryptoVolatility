FROM hadoop-base:latest

# Check if the namenode is running
HEALTHCHECK CMD curl -f http://localhost:9870/ || exit 1

RUN mkdir -p /hadoop/dfs/name
VOLUME /hadoop/dfs/name

EXPOSE 9870

# Format the namenode if it is not formatted and start the namenode
CMD ["bash", "-c", "if [ -z \"$(ls -A /hadoop/dfs/name)\" ]; then \
    $HADOOP_HOME/bin/hdfs --config $HADOOP_CONF_DIR namenode -format; \
  fi && \
  $HADOOP_HOME/bin/hdfs --config $HADOOP_CONF_DIR namenode"]