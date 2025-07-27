.PHONY: default init lint run doc serve clean

ifeq ($(OS),Windows_NT)
# On Windows CMD, run: make run PYTHON=python PIP=pip
PYTHON ?= python
PIP ?= pip
else
# On Unix-like systems, use python3 and pip3 by default
PYTHON ?= python3
PIP ?= pip3
endif

default: init lint doc

init:	
	$(PIP) install -r requirements.txt

lint:
	$(PYTHON) -m black .
	$(PYTHON) -m pylint src

run:
	$(PYTHON) src/effect_player/effect_player.py

doc:
	$(PYTHON) -m mkdocs build

serve:
	$(PYTHON) -m mkdocs serve

clean:
	rm -rf build dist __pycache__ *.spec

all: init lint doc run