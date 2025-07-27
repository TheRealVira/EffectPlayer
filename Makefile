.PHONY: default init lint run doc serve clean
PROGRAM_NAME = python
PROGRAM = src/effect_player/effect_player.py

default: init lint doc

init:	
	pip install -r requirements.txt

lint:
	black .
	pylint src

run:
	${PROGRAM_NAME} ./${PROGRAM} ${ARGS}

doc:
	mkdocs build

serve:
	mkdocs serve

clean:
	rm -rf build dist __pycache__ *.spec

all: init lint doc run