# Makefile for manage the project docker and docker-compose

.PHONY: help
#.PHONY: default

default: build;

## Run build process on both environments
all: build

## Start containers in detached mode
start: build
	docker compose up -d

## Stop containers but won't remove them
stop:
	docker compose stop

## Run build process on both environments
build:
	cp .env.dist .env
	docker compose build

## Run containers in detached mode
up:
	docker compose up --detach --remove-orphans --build

## Stop containers and will remove them
down:
	docker compose down

## Show logs of all containers
logs:
	docker compose logs -f --tail=500

logs-app:
	docker compose logs -f --tail=500 app

## Kill all containers
kill:
	docker compose kill

## Restart all containers
restart: stop up

## Remove all containers, images, volumes and networks
clean:
	docker compose down --rmi all --volumes --remove-orphans

## Show status of all containers
ps:
	docker compose ps

## Show status of all containers
exec:
	docker compose exec api bash

## Run tests
tests:
	docker compose exec app pytest -v tests/


## help: Show this help message
help:
	@echo $$'Available targets:\n'
	@grep -e "^##" -A1 $(MAKEFILE_LIST) | \
		sed -e "/^--$\/d; s/\:.*$\//g; s/\#\#\s*//g" | \
		awk '{if(NR%2 == 0) {printf("\t%-16s\t%s\n", $$0, f)} { f=$$0 }}'
