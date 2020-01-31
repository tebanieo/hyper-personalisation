SHELL := /bin/bash
BUILD_VERSION := ${BUILD_VERSION}
OUTPUT ?= ../output
DB_TABLE_NAME ?= operationalHours-local
DB_ENDPOINT ?= http://localhost:8000

prepare:
	mkdir ${OUTPUT}

clean:
	rm -rvf ${OUTPUT}

compile: .
	make compile/retrieveConnectInfo

compile-local: .
	chmod +x sam-local-retrieveConnectInfo.sh
	./sam-local-retrieveConnectInfo.sh

compile/retrieveConnectInfo:
	cd ../lambdaFunctions/retrieveConnectInfo && zip -r -j retrieveConnectInfo.zip .
	mv ../lambdaFunctions/retrieveConnectInfo/retrieveConnectInfo.zip ${OUTPUT}/retrieveConnectInfo.zip

start/sam: .
	make compile-local
	nohup sam local start-lambda -t ./dist/template.local.yaml &

start/sam-debug: .
	sam local start-lambda -t ./infra/dist/template.local.yaml

test/unit: .
	yarn test

#test/functional: .
#	make compile && \
#	make start/services && \
#	yarn test:func && \
#	make stop/services

build: .
	make prepare
	#make test/unit
	#make test/functional
	make compile

start/services: .
	make start/sam
	make start/db

stop/services: .
	make stop/sam
	make stop/db

start/sam-debug: .
	sam local start-lambda -t ./infra/dist/template.local.yaml

stop/sam: .
	lsof -i tcp:3001 -t | xargs kill

start/db: .
	docker run --detach --name dynamodb-local-operational-hours --publish 8000:8000 amazon/dynamodb-local
	make create/table
	make populate/table

stop/db: .
	docker ps --quiet --filter "name=dynamodb-local-operational-hours" | xargs docker stop | xargs docker rm

create/table: .
	aws dynamodb create-table \
        --table-name ${DB_TABLE_OP_NAME} \
        --attribute-definitions \
            AttributeName=hoursKey,AttributeType=S \
        --key-schema \
            AttributeName=hoursKey,KeyType=HASH \
            --provisioned-throughput \
            ReadCapacityUnits=10,WriteCapacityUnits=5 \
            --endpoint-url ${DB_ENDPOINT}

populate/table: .
	aws dynamodb batch-write-item \
        --request-items file://../server/tests/functional/db-content/ophours.json \
        --endpoint-url ${DB_ENDPOINT}

delete/table: .
	aws dynamodb delete-table \
    	--table-name ${DB_TABLE_OP_NAME} \
    	--endpoint-url ${DB_ENDPOINT}

scan/table: .
	aws dynamodb scan \
	    --table-name ${DB_TABLE_OP_NAME} \
	    --endpoint-url ${DB_ENDPOINT}
