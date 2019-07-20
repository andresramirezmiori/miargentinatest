help:
	@echo "help  -- print this help"
	@echo "start -- start docker stack"
	@echo "stop  -- stop docker stack"
	@echo "ps    -- show status"
	@echo "dockershell -- run bash inside docker"
	@echo "shell_plus -- run django shell_plus inside docker"

RUN=docker-compose exec web
MANAGE=${RUN} ./manage.py

build:
	docker-compose build

start:
	docker-compose up -d
	${MANAGE} migrate
	${MANAGE} runserver 0.0.0.0:8000

createsuperuser:
	${MANAGE} createsuperuser

up:
	docker-compose up -d

stop:
	docker-compose stop

ps:
	docker-compose ps

clean:
	docker-compose down

dockershell:
	${RUN} /bin/bash

migrations:
	${MANAGE} makemigrations

migrate:
	${MANAGE} migrate

collectstatic:
	${MANAGE} collectstatic

shell_plus:
	${MANAGE} shell_plus

.PHONY: help start stop ps clean test dockershell shell_plus only_test pep8
