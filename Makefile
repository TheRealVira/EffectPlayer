PROGRAM_NAME = python
PROGRAM = src/effect_player/effect_player.py

default: all

init:	
	pip install -r requirements.txt

doc
	mkdocs build

lint:
	pylint src

run:
	${PROGRAM_NAME} ./${PROGRAM} ${ARGS}

all: init lint run

.PHONY: test doc lint