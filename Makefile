#! /usr/bin/env make
APP_ROOT_PATH := ./app
TESTS_PATH := ./tests
TESTS_EVENTS_PATH := ${TESTS_PATH}/events
LOCALSTACK_IMAGE := "localstack/localstack:1.2.0"
LOCALSTACK_CONTAINER_NAME := "workshop-unit-testing"

install:
	@pip install -r ${APP_ROOT_PATH}/requirements.txt
	@pip install -r ${TESTS_PATH}/requirements.txt

localstack-start: localstack-stop
	@echo ">>> Starting localstack in detached mode"
	@docker run -d \
	-e DEBUG=1 \
	-e AWS_ACCESS_KEY_ID=foo \
	-e AWS_SECRET_ACCESS_KEY=bar \
	-e DEFAULT_REGION=eu-central-1 \
	-e HOSTNAME=localstack \
	-e HOSTNAME_EXTERNAL=localstack \
	-e LOCALSTACK_HOST=localstack \
	-e TEST_AWS_ACCOUNT_ID=000000000000 \
	-v "/tmp/localstack:/tmp/localstack" \
	-v "/var/run/docker.sock:/var/run/docker.sock" \
	-p 4566:4566 \
	-p 4571:4571 \
	--name=${LOCALSTACK_CONTAINER_NAME} \
	${LOCALSTACK_IMAGE}

	@python ./build/localstack.py

localstack-stop:
	@echo ">>> Stopping container if it is running"
	if [ $(shell docker container ls --filter NAME=${LOCALSTACK_CONTAINER_NAME} -aq | wc -l) -eq 1 ]; then \
		docker stop ${LOCALSTACK_CONTAINER_NAME}; \
		docker rm ${LOCALSTACK_CONTAINER_NAME}; \
	fi
	@echo ">>> Done"

run: localstack-start
	export PYTHONPATH=${APP_ROOT_PATH} \
	&& python app/main.py

unit-tests:
	export PYTHONPATH=${APP_ROOT_PATH} \
	&& pytest --cov-report term-missing --cov-config=.coveragerc --cov=${APP_ROOT_PATH}

default: install
