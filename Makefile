DOCKER=docker-compose

.PHONY: init up stop down

init:
	@$(DOCKER) up -d --build

up:
	@$(DOCKER) up -d

stop:
	@$(DOCKER) stop

down:
	@$(DOCKER) down --remove-orphans