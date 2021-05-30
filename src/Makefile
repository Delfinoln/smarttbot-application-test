TAG=0.0.1
IMAGE_SOCKET=poloniex_socket
IMAGE_CONSUMER=poloniex_enrich

.PHONY: help
help: ## Show help menu
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "%-35s\033 %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: docker-build
docker-build: ## Build docker base image
	docker build --target ${IMAGE_SOCKET} . -t ${IMAGE_SOCKET}:${TAG}
	docker build --target ${IMAGE_CONSUMER} . -t ${IMAGE_CONSUMER}:${TAG}

.PHONY: docker-run
docker-run: ## Run Docker image (just for local tests)
	docker run -p 9000:9000 -ti ${IMAGE_SOCKET}:${TAG} &
	docker run -p 9001:9001 -ti ${IMAGE_CONSUMER}:${TAG}

.PHONY: docker-compose
docker-compose: ## Run docker-compose
	docker-compose -f docker-compose.yaml up

.PHONY: all
all: docker-build docker-compose ## Build image and run docker-compose
