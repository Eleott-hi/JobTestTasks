export PYTHONUNBUFFERED=1
export PYTHONPYCACHEPREFIX=build
export PYTHONPATH=.

ENV := . .env/bin/activate

PIPE := cat test.txt | grep -v "# GREP" 

all: run

install:
	pip install -r requirements.txt

# run:
# 	$(PIPE) | python3 app/main.py
# run:
# 	python3 app/main.py

run:
	python3 src/main.py

test:
	pytest tests -q