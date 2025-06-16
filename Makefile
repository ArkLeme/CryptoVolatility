DEPS_DIR = output/
AWS_BUCKET = crypto-volatility-prod

.PHONY: all deps upload apply clean

all: build upload terraform

build:
	mkdir -p $(DEPS_DIR)
	docker build -t spark-apps-packager -f spark_apps/Dockerfile spark_apps
	docker run --rm -v "$(PWD)/$(DEPS_DIR):/output" spark-apps-packager

upload:
	aws s3 cp spark_apps/schema/binance_crypto_kline.yml s3://$(AWS_BUCKET)/schema/
	aws s3 cp spark_apps/schema/binance_crypto_hourly_volatility.yml s3://$(AWS_BUCKET)/schema/
	aws s3 cp spark_apps/bin/ingest_binance.py s3://$(AWS_BUCKET)/code/
	aws s3 cp spark_apps/bin/process_volatility.py s3://$(AWS_BUCKET)/code/
	aws s3 cp $(DEPS_DIR)/deps.zip s3://$(AWS_BUCKET)/deps/deps.zip

terraform:
	cd terraform && terraform init && terraform plan && terraform apply -auto-approve

clean:
	rm -rf $(DEPS_DIR)
