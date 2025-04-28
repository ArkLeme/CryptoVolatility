FROM hadoop-base:latest

# Install PostgreSQL client
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Hive setup
ENV HIVE_VERSION=4.0.0
ENV HIVE_HOME=/opt/hive
ENV PATH=$PATH:$HIVE_HOME/bin

RUN wget https://archive.apache.org/dist/hive/hive-$HIVE_VERSION/apache-hive-$HIVE_VERSION-bin.tar.gz \
    && tar -xzf apache-hive-${HIVE_VERSION}-bin.tar.gz -C /opt \
    && mv /opt/apache-hive-${HIVE_VERSION}-bin $HIVE_HOME \
    && rm apache-hive-${HIVE_VERSION}-bin.tar.gz

# Add PostgreSQL JDBC driver
RUN wget https://jdbc.postgresql.org/download/postgresql-42.6.0.jar -P $HIVE_HOME/lib/

# Copy Hive configuration
COPY ../config/hive-site.xml $HIVE_HOME/conf/
COPY ../config/hive-env.sh $HIVE_HOME/conf/

# Copy run scripts
COPY run_metastore.sh /run_metastore.sh
COPY run_server.sh /run_server.sh
RUN chmod +x /run_metastore.sh
RUN chmod +x /run_server.sh