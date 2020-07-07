SHELL = /bin/bash

.DEFAULT_GOAL := help

CURRENT_DIR := $(shell pwd)
INSTALL_DIR := $(CURRENT_DIR)/.venv
PYTHON_FILES := $(shell find ./* -type f -name "*.py" -print)

#FIXME: put this variable in config file
PYTHON_VERSION=3.7.4
CURRENT_PYTHON_VERSION := $(shell python3 -c "import sys;t='{v[0]}.{v[1]}.{v[2]}'.format(v=list(sys.version_info[:]));sys.stdout.write(t)")
PYTHON_VERSION_OK := $(shell python3 -c "import sys; t=sys.version_info[0:3]; print(int('{}.{}.{}'.format(*t) == '$(PYTHON_VERSION)'))")

# Commands
SYSTEM_PYTHON_CMD := $(shell which python3)
PYTHON_CMD := $(INSTALL_DIR)/bin/python3
PIP_CMD := $(INSTALL_DIR)/bin/pip3
FLASK_CMD := $(INSTALL_DIR)/bin/flask
YAPF_CMD := $(INSTALL_DIR)/bin/yapf
all: help

# This bit check define the build/python "target": if the system has an acceptable version of python, there will be no need to install python locally.

ifeq ($(PYTHON_VERSION_OK),1)
PYTHON_BINDIR := $(shell dirname $(PYTHON_CMD))
PYTHONHOME := $(shell eval "cd $(PYTHON_BINDIR); pwd; cd > /dev/null")
build/python:
		@echo $(CURRENT_PYTHON_VERSION)
		@echo $(shell $(PYTHON_CMD) -c "print('OK')")
		mkdir -p build
		touch build/python;
else
build/python: local/bin/python3.7
	mkdir -p build
	touch build/python;

SYSTEM_PYTHON_CMD := $(CURRENT_DIR)/local/bin/python3.7
endif



.PHONY: help
help:
	@echo "Usage: make <target>"
	@echo
	@echo "Possible targets:"
	@echo -e " \033[1mBUILD TARGETS\033[0m "
	@echo "- setup			Create the python virtual environment"
	@echo -e " \033[1mLINTING TOOLS TARGETS\033[0m "
	@echo "- lint			Lint the python source code"
	@echo -e " \033[1mLOCAL SERVER TARGETS\033[0m "
	@echo "- serve			Run the project using the flask debug server"
	@echo "- gunicornserve		Run the project using the gunicorn WSGI server"
	@echo "- dockerrun		Run the project using the gunicorn WSGI server inside a container. Env variable HTTP_PORT should be set"
	@echo "- shutdown		Stop the aforementioned container"
	@echo -e " \033[1mCLEANING TARGETS\033[0m "
	@echo "- clean			Clean genereated files"
	@echo "- clean_venv		Clean python venv"

# Build targets. Calling setup is all that is needed for the local files to be installed as needed. Bundesnetz may cause problem.

python: build/python
	@echo "Python installed"

.PHONY: setup
setup: python .venv/build.timestamp


local/bin/python3.7:
	mkdir -p $(CURRENT_DIR)/local;
	curl -z $(CURRENT_DIR)/local/Python-$(PYTHON_VERSION).tar.xz https://www.python.org/ftp/python/$(PYTHON_VERSION)/Python-$(PYTHON_VERSION).tar.xz -o $(CURRENT_DIR)/local/Python-$(PYTHON_VERSION).tar.xz;
	cd $(CURRENT_DIR)/local && tar -xf Python-$(PYTHON_VERSION).tar.xz && Python-$(PYTHON_VERSION)/configure --prefix=$(CURRENT_DIR)/local/ && make altinstall

.venv/build.timestamp: build/python
	$(SYSTEM_PYTHON_CMD) -m venv $(INSTALL_DIR) && $(PIP_CMD) install --upgrade pip setuptools
	${PIP_CMD} install -r dev_requirements.txt
	$(PIP_CMD) install -r requirements.txt
	touch .venv/build.timestamp

# linting target, calls upon yapf to make sure your code is easier to read and respects some conventions.

.PHONY: lint
lint: .venv/build.timestamp
		$(YAPF_CMD) -i --style .style.yapf $(PYTHON_FILES)

# Serve targets. Using these will run the application on your local machine. You can either serve with a wsgi front (like it would be within the container), or without.
.PHONY: serve
serve: .venv/build.timestamp
		FLASK_APP=service_name FLASK_DEBUG=1 ${FLASK_CMD} run --host=0.0.0.0 --port=${SERVICE_QR_CODE_HTTP_PORT}

.PHONY: gunicornserve
gunicornserve: .venv/build.timestamp
		${SYSTEM_PYTHON_CMD} wsgi.py


# Docker related functions.

.PHONY: dockerrun
dockerrun:
	docker-compose up -d;
	sleep 10

.PHONY: shutdown
shutdown:
	docker-compose down

# Cleaning functions. clean_venv will only remove the virtual environment, while clean will also remove the local python installation.

.PHONY: clean
clean: clean_venv
	rm -rf local;

.PHONY: clean_venv
clean_venv:
	rm -rf ${INSTALL_DIR};
