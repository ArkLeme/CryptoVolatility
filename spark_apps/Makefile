SPARK_CONFIG = spark.conf
INGEST_SCRIPT = bin/ingest_binance.py
VOLATILITY_SCRIPT = bin/process_volatility.py

INGEST_SCHEMA_PATH = schema/binance_crypto_kline.yml
VOLATILITY_SCHEMA_PATH = schema/binance_crypto_hourly_volatility.yml

SYMBOL = BTCUSDT
DATE = $(shell date +%Y-%m-%d)

install:
	uv venv
	source .venv/bin/activate
	uv pip install ."[binance]" --group local

run_ingest:
	@echo "Running ingestion for symbol: $(SYMBOL) on date: $(DATE)"
	HADOOP_CONF_DIR=/dev/null YARN_CONF_DIR=/dev/null spark-submit --properties-file $(SPARK_CONFIG) $(INGEST_SCRIPT) \
		--schema_path $(INGEST_SCHEMA_PATH) \
		--date $(DATE) \
		--symbol $(SYMBOL)

run-volatility:
	@echo "Running volatility processing for symbol: $(SYMBOL) on date: $(DATE)"
	HADOOP_CONF_DIR=/dev/null YARN_CONF_DIR=/dev/null spark-submit --properties-file $(SPARK_CONFIG) $(VOLATILITY_SCRIPT) \
		--schema_path $(VOLATILITY_SCHEMA_PATH) \
		--date $(DATE) \
		--symbol $(SYMBOL)

test:
	uv pip install .[test]
	pytest

.PHONY: run_ingest run-volatility 