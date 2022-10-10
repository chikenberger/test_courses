DOCKER=docker-compose
DB=python3 manage.py

.PHONY: init up down migrations migrate

init:
	@$(DOCKER) up -d --build

up:
	@$(DOCKER) up -d

down:
	@$(DOCKER) down --remove-orphans

migrations:
	@$(DB) makemigrations

migrate:
	@$(DB) migrate