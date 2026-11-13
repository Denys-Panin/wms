.DEFAULT_GOAL := help

COMPOSE := docker compose
WEB := web
DB := db
MANAGE := $(COMPOSE) exec $(WEB) python manage.py
PYTHON := $(COMPOSE) exec $(WEB) python

.PHONY: help rb u d r lw ld sh \
        m mm su t ch\
		lc lf fc f
    	

help:
	@echo "Available commands:"
	@echo "  make rb                          Rebuild Docker images and start containers"
	@echo "  make u                           Start containers"
	@echo "  make d                           Stop containers"
	@echo "  make r                           Restart containers"
	@echo "  make lw                          Show web logs"
	@echo "  make ld                          Show db logs"
	@echo "  make sh                          Open Django shell_plus"
	@echo "  make mm                          Create migrations"
	@echo "  make mm APP=app_name             Create migrations for a specific app"
	@echo "  make m                           Apply migrations"
	@echo "  make m APP=app_name              Apply migrations for a specific app"
	@echo "  make su                          Create superuser"
	@echo "  make t                           Run all tests"
	@echo "  make t TEST_PATH=path_to_file    Run specific tests"
	@echo "  make ch                          Run Django system checks"
	@echo "  make lc                          Check code-quality problems"
	@echo "  make lf                         Automatically fix supported lint issues"
	@echo "  make fc                          Check formatting without modifying files"
	@echo "  make f                           Format Python code"

rb:
	$(COMPOSE) up -d --build

u:
	$(COMPOSE) up -d

d:
	$(COMPOSE) down

r:
	$(COMPOSE) restart

lw:
	$(COMPOSE) logs -f $(WEB)

ld:
	$(COMPOSE) logs -f $(DB)

sh:
	$(MANAGE) shell_plus

m:
	$(MANAGE) migrate $(APP)

mm:
	$(MANAGE) makemigrations $(APP)

su:
	$(MANAGE) createsuperuser

t:
	$(PYTHON) -m pytest $(TEST_PATH) -v

ch:
	$(MANAGE) check

# RUFF
lc:
	$(COMPOSE) exec $(WEB) ruff check .

lf:
	$(COMPOSE) exec $(WEB) ruff check . --fix

fc:
	$(COMPOSE) exec $(WEB) ruff format --check .

f:
	$(COMPOSE) exec $(WEB) ruff format . 


