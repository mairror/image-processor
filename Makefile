SHELL := /usr/bin/bash
.DEFAULT_GOAL := help

# AutoDoc
# -------------------------------------------------------------------------
.PHONY: help
help: ## This help. Please refer to the Makefile to more insight about the usage of this script.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
.DEFAULT_GOAL := help

# Docker
# -------------------------------------------------------------------------

# PROCESSOR
# -------------------------------------------------------------------------
.PHONY: build-docker-processor
build-docker-processor: ## Build the PROCESSOR Dockerfile. Optional variables BUILDKIT, DOCKER_PROCESSOR_IMAGE and DOCKER_PROCESSOR_TAG
	export BUILDKIT=$(or $(BUILDKIT_ENABLED),1) \
		DOCKER_PROCESSOR_IMAGE=$(or $(DOCKER_PROCESSOR_IMAGE),mairror-processor) \
		DOCKER_PROCESSOR_TAG=$(or $(DOCKER_PROCESSOR_TAG),test) && \
	docker build -t $$DOCKER_PROCESSOR_IMAGE:$$DOCKER_PROCESSOR_TAG .
.DEFAULT_GOAL := build-docker-processor

.PHONY: lint-docker-processor
lint-docker-processor: ## Lint the PROCESSOR Dockerfile
	docker run --rm -i -v ${PWD}:/hadolint --workdir=/hadolint hadolint/hadolint < Dockerfile
.DEFAULT_GOAL := lint-docker-processor

.PHONY: run-docker-processor
run-docker-processor: ## Run the PROCESSOR isolated. Optional variables BUILDKIT, DOCKER_PROCESSOR_IMAGE and DOCKER_PROCESSOR_TAG
	export BUILDKIT=$(or $(BUILDKIT_ENABLED),1) \
		DOCKER_PROCESSOR_IMAGE=$(or $(DOCKER_PROCESSOR_IMAGE),mairror-processor) \
		DOCKER_PROCESSOR_TAG=$(or $(DOCKER_PROCESSOR_TAG),test) && \
	docker run --rm --name $$DOCKER_PROCESSOR_IMAGE --env-file .env -p 8000:8000 $$DOCKER_PROCESSOR_IMAGE:$$DOCKER_PROCESSOR_TAG
.DEFAULT_GOAL := run-docker-processor

# Python
# -------------------------------------------------------------------------

# Cache
# -------------------------------------------------------------------------
.PHONY: clean-pyc
clean-pycache: ## Clean pycache files

	find . -name '__pycache__' -exec rm -rf {} +
.DEFAULT_GOAL := clean-pyc
