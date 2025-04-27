FROM hadoop-base:latest

HEALTHCHECK CMD curl -f http://localhost:8042/ || exit 1

EXPOSE 8042

CMD ["bash", "-c", "$HADOOP_HOME/bin/yarn --config $HADOOP_CONF_DIR nodemanager"]