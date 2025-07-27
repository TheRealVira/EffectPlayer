.PHONY: default init lint run doc serve clean

PYTHON ?= python
PIP ?= pip

default: init lint doc

init:	
	$(PIP) install -r requirements.txt

lint:
	$(PYTHON) -m black .
	$(PYTHON) -m pylint src

run:
	set PYTHONPATH=src && $(PYTHON) -m effect_player.effect_player

doc:
	$(PYTHON) -m mkdocs build

serve:
	$(PYTHON) -m mkdocs serve

clean:
	rm -rf build dist __pycache__ *.spec

all: init lint doc run