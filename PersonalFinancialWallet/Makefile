export PYTHONUNBUFFERED=1
export PYTHONPYCACHEPREFIX=build
export PYTHONPATH=.

ENV := . .env/bin/activate

PIPE := cat test.txt | grep -v "# GREP" 

all: test run

install:
	pip install -r requirements.txt

run:
	python3 app/main.py

test:
	clear
	pytest tests -q --cov=app --cov-report html