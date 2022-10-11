DOCKER=docker-compose
DB=python3 manage.py

.PHONY: init up stop down migrations migrate

init:
	@$(DOCKER) up -d --build

up:
	@$(DOCKER) up -d

stop:
	@$(DOCKER) stop

down:
	@$(DOCKER) down --remove-orphans

migrations:
	@$(DB) makemigrations

migrate:
	@$(DB) migrate