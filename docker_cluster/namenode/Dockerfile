FROM hadoop-base:latest

HEALTHCHECK CMD curl -f http://localhost:9870/ || exit 1

RUN mkdir -p /hadoop/dfs/name
VOLUME /hadoop/dfs/name

EXPOSE 9870

CMD ["bash", "-c", "if [ -z \"$(ls -A /hadoop/dfs/name)\" ]; then \
    $HADOOP_HOME/bin/hdfs --config $HADOOP_CONF_DIR namenode -format; \
  fi && \
  $HADOOP_HOME/bin/hdfs --config $HADOOP_CONF_DIR namenode"]