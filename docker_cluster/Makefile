build-cluster:
	docker-compose build

start-cluster:
	docker-compose up -d

stop-cluster:
	docker-compose down

clean-cluster:
	docker-compose down --volumes

logs:
	docker-compose logs -f

.PHONY: build-cluster start-cluster stop-cluster clean-cluster logs