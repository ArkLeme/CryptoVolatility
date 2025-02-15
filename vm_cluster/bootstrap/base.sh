#!/bin/bash
sudo apt-get update -y
sudo apt-get install -y openjdk-8-jdk ssh wget

# Set environment variables
echo "export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64" >> /home/hadoop/.bashrc
echo "export HADOOP_HOME=/opt/hadoop" >> /home/hadoop/.bashrc
echo "export PATH=\$HADOOP_HOME/bin:\$HADOOP_HOME/sbin:\$PATH" >> /home/hadoop/.bashrc
echo "export HADOOP_CONF_DIR=\$HADOOP_HOME/etc/hadoop" >> /home/hadoop/.bashrc

# Install Hadoop
HADOOP_VERSION=3.3.6
HADOOP_HOME=/opt/hadoop
wget https://dlcdn.apache.org/hadoop/common/hadoop-$HADOOP_VERSION/hadoop-$HADOOP_VERSION.tar.gz
tar -xvzf hadoop-$HADOOP_VERSION.tar.gz -C /opt
mv /opt/hadoop-$HADOOP_VERSION $HADOOP_HOME

# Configure hosts file
echo "127.0.0.1 localhost" > /etc/hosts
echo "192.168.56.10 namenode" >> /etc/hosts
echo "192.168.56.11 datanode1" >> /etc/hosts