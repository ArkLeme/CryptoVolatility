FROM hadoop-base:latest

# Check if the historyserver is running
HEALTHCHECK CMD curl -f http://localhost:8188/ || exit 1

RUN mkdir -p /hadoop/yarn/timeline
VOLUME /hadoop/yarn/timeline

EXPOSE 8188

CMD ["bash", "-c", "$HADOOP_HOME/bin/yarn --config $HADOOP_CONF_DIR historyserver"]