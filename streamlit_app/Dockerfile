FROM ubuntu:20.04

# Prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install Python and other dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-dev \
    openjdk-8-jdk \
    libsasl2-dev \
    libsasl2-modules \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
ENV PATH=$PATH:$JAVA_HOME/bin
ENV PYTHONPATH=/app/src
ENV HIVE_WAREHOUSE_DIR=/user/hive/warehouse
ENV HIVE_METASTORE_URI=thrift://hivemetastore:9083

ENV SPARK_HOME=/app/.venv/lib/python3.8/site-packages/pyspark
ENV HADOOP_CONF_DIR=/opt/hadoop/etc/hadoop
ENV YARN_CONF_DIR=/opt/hadoop/etc/hadoop

# Create app directory
WORKDIR /app

# Install uv
RUN pip install uv
RUN uv venv
# Copy project files
COPY pyproject.toml .
RUN uv pip install ".[streamlit]" --group local

# Copy source code
COPY streamlit_app/ /src

# Expose Streamlit port
EXPOSE 8501

# Set the entrypoint
# ENTRYPOINT ["uv", "run", "streamlit", "run", "/app/src/app.py"]
CMD ["sleep", "3600"]