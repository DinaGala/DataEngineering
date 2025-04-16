SHELL := /bin/bash

D_PS = $(shell docker ps -aq)
D_IMG = $(shell docker images -q)
VENV_DIR := .venv
PYTHON := $(VENV_DIR)/bin/python
PIP := $(VENV_DIR)/bin/pip
PGADMIN_PY := $(shell find $(VENV_DIR)/lib -name "pgAdmin4.py")

DOCKER_COMPOSE = docker-compose -f ./docker-compose.yml

all: build up install

build:
	@$(DOCKER_COMPOSE) build


up:
	@$(DOCKER_COMPOSE) up --detach --remove-orphans

venv:
	@echo "Creating virtual environment..."
	python3 -m venv $(VENV_DIR)

install: venv
	@echo "Installing dependencies..."
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	cp config_local.py $(VENV_DIR)/lib/python3.10/site-packages/pgadmin4/config_local.py
	$(PYTHON) $(PGADMIN_PY)

ex02:
	@echo "Creating a table..."
	$(PYTHON) ./ex02/table.py

ex03:
	@echo "Creating an automated table..."
	$(PYTHON) ./ex03/automatic_table.py

#stop -> stops services
stop:
	@$(DOCKER_COMPOSE) stop

#down -> stops and removes containers and networks
down:
	@$(DOCKER_COMPOSE) down

clean: down
	@$(DOCKER_COMPOSE) rm
# rm -rf $(VENV_DIR)

ps:
	@$(DOCKER_COMPOSE) ps

ls:
	docker volume ls

fclean: down
	@if [ -n "$(D_PS)" ]; then \
		echo "deleting containers"; \
		docker stop $(D_PS); \
		docker rm $(D_PS); \
	fi
	@if [ -n "$(D_IMG)" ]; then \
		echo "deleting images"; \
		docker rmi $(D_IMG); \
	fi
	@if [ -n "$$(docker volume ls -q --filter dangling=true)" ]; then \
		echo "deleting volumes"; \
		docker volume rm $$(docker volume ls -q --filter dangling=true); \
		docker system prune -a --volumes; \
		echo "volumes deleted"; \
	fi


re: fclean all up

.PHONY: all build up clean fclean