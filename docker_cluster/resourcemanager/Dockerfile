FROM hadoop-base:latest

HEALTHCHECK CMD curl -f http://localhost:8088/ || exit 1

EXPOSE 8088

CMD ["bash", "-c", "$HADOOP_HOME/bin/yarn --config $HADOOP_CONF_DIR resourcemanager"]