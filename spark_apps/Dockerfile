FROM amazonlinux:2

RUN yum install -y \
    gcc \
    openssl11 \
    openssl11-devel \
    bzip2-devel \
    libffi-devel \
    tar \
    gzip \
    wget \
    make

RUN wget https://www.python.org/ftp/python/3.8.20/Python-3.8.20.tgz && \
    tar xzf Python-3.8.20.tgz && \
    cd Python-3.8.20 && \
    ./configure --enable-optimizations && \
    make altinstall && \
    cd .. && \
    rm -rf Python-3.8.20.tgz Python-3.8.20

RUN python3.8 -m ensurepip && \
    python3.8 -m pip install uv

WORKDIR /app

RUN uv venv 
RUN cp -r /usr/local/lib/python3.8/* ./.venv/lib/python3.8

COPY crypto_volatility/*.py ./crypto_volatility/
COPY pyproject.toml ./

RUN source ./.venv/bin/activate && \
    uv pip install .["binance","aws"] && \
    uv pip install venv-pack && \
    venv-pack -f -o deps.zip --python-prefix /home/hadoop/environment

CMD ["cp", "deps.zip", "/output/deps.zip"]
