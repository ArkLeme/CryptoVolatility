FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

# Install packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-8-jdk \
    wget \
    curl \
    netcat \
    gnupg \
    net-tools \
    python3 \
    python3-pip \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Setup Java environment variables
ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
ENV PATH=$PATH:$JAVA_HOME/bin

# Setup Hadoop environment variables
ENV HADOOP_HOME=/opt/hadoop
ENV HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
ENV PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

# Setup Hadoop version and URL
ENV HADOOP_VERSION 3.3.6
ENV HADOOP_URL https://dlcdn.apache.org/hadoop/common/hadoop-$HADOOP_VERSION/hadoop-$HADOOP_VERSION.tar.gz

# Download and verify Hadoop release (https://hadoop.apache.org/releases.html)
RUN curl -O https://downloads.apache.org/hadoop/common/KEYS \
    && gpg --import KEYS \
    && curl -fSL "$HADOOP_URL" -o /tmp/hadoop.tar.gz \
    && curl -fSL "$HADOOP_URL.asc" -o /tmp/hadoop.tar.gz.asc \
    && gpg --verify /tmp/hadoop.tar.gz.asc \
    && tar -xf /tmp/hadoop.tar.gz -C /opt/ \
    && rm /tmp/hadoop.tar.gz* KEYS

# Setup Hadoop 
RUN mv /opt/hadoop-$HADOOP_VERSION $HADOOP_HOME
RUN ln -s $HADOOP_HOME/etc/hadoop /etc/hadoop

# Set working directory
WORKDIR $HADOOP_HOME

# Copy configuration files
COPY config/* $HADOOP_CONF_DIR/