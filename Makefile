NAME := security-sandbox
INSTALL_STAMP := .install.stamp
POETRY := $(shell command -v poetry 2> /dev/null)
.DEFAULT_GOAL := help

.PHONY: help
help:
		@echo "Please use 'make <target>' where <target> is one of"
		@echo ""
		@echo "  install     install packages and prepare environment"
		@echo "  clean       remove all temporary files"
		@echo "  lint        run the code linters"
		@echo "  format      reformat code"
		@echo "  test        run all the tests"
		@echo ""
		@echo "Check the Makefile to know exactly what each target is doing."

install: $(INSTALL_STAMP)
$(INSTALL_STAMP): pyproject.toml poetry.lock
		@if [ -z $(POETRY) ]; then echo "Poetry could not be found. See https://python-poetry.org/docs/"; exit 2; fi
		$(POETRY) install
		touch $(INSTALL_STAMP)

.PHONY: clean
clean:
		find . -type d -name "__pycache__" | xargs rm -rf {};
		rm -rf $(INSTALL_STAMP) .coverage .mypy_cache

.PHONY: lint
lint: $(INSTALL_STAMP)
		$(POETRY) run isort --profile=black --lines-after-imports=2 --check-only ./tests/ $(NAME)
		$(POETRY) run black --check ./tests/ $(NAME) --diff
		$(POETRY) run flake8 --ignore=W503,E501 ./tests/ $(NAME)
		$(POETRY) run mypy ./tests/ $(NAME) --ignore-missing-imports
		$(POETRY) run bandit -r $(NAME) -s B608

.PHONY: format
format: $(INSTALL_STAMP)
		$(POETRY) run isort --profile=black --lines-after-imports=2 ./tests/ runnables configs
		$(POETRY) run black ./tests/ runnables configs

.PHONY: test
test: $(INSTALL_STAMP)
		$(POETRY) run pytest ./tests/ --cov-report term-missing --cov-fail-under 0 --cov $(NAME)

.PHONY: run_test_server
run_test_server: $(INSTALL_STAMP)
		$(POETRY) run python runnables/run_test_lidar_server.py \
			--host 0.0.0.0 --port 3000 --n_channels 4

.PHONY: run_test_server_without_poetry
run_test_server_without_poetry:
		python3 runnables/run_test_lidar_server.py \
			--host 0.0.0.0 --port 3000 --n_channels 4

.PHONY: run_test_client
run_test_client: $(INSTALL_STAMP)
		$(POETRY) run python runnables/run_test_lidar_client.py \
			--host 0.0.0.0 --port 3000 --n_channels 4

.PHONY: run_attacker_passthrough
run_attacker_passthrough: $(INSTALL_STAMP)
		$(POETRY) run python runnables/run_lidar_attacker.py \
			configs/lidar_passthrough.yml \
			--host 0.0.0.0 --port 3000 --n_channels 4

.PHONY: run_attacker_fp
run_attacker_fp: $(INSTALL_STAMP)
		$(POETRY) run python runnables/run_lidar_attacker.py \
			configs/lidar_fp_attacker.yml \
			--host 0.0.0.0 --port 3000 --n_channels 4