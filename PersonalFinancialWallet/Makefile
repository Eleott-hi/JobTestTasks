export PYTHONUNBUFFERED=1
export PYTHONPYCACHEPREFIX=build
export PYTHONPATH=.

all: install run

install:
	pip install -r requirements.txt

run:
	cat test.txt | grep -v "# GREP" | python3 app/main.py
# run:
# 	python3 app/main.py
