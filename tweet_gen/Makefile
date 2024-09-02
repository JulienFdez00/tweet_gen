USE_CONDA ?= 1
INSTALL_SCRIPT = install_virtual_env/install_with_conda.sh
ifeq (false,$(USE_CONDA))
	INSTALL_SCRIPT = install_virtual_env/install_with_venv.sh
endif

.DEFAULT_GOAL = help

# help: help				      - Display this makefile's help information
.PHONY: help
help:
	@grep "^# help\:" Makefile | grep -v grep | sed 's/\# help\: //' | sed 's/\# help\://'

# help: install_precommit			- Install pre-commit hooks
.PHONY: install_precommit
install_precommit:
	@pre-commit install -t pre-commit
	@pre-commit install -t pre-push

# help: pre_commit	                       - Run pre-commit hooks
.PHONY: pre_commit
pre_commit:
	@pre-commit run --all-files --hook-stage pre-push --show-diff-on-failure

# help: run_backend			        - Run backend API (defalut port 8000 if not specified)
.PHONY: run_backend
run_backend:
	@PYTHONPATH=. python backend/main.py

# help: run_frontend		                - Run Frontend streamlit app (defalut port 8501 if not specified)
.PHONY: run_frontend
run_frontend:
	@PYTHONPATH=. streamlit run frontend/app.py
