export PYTHONUNBUFFERED=1
export PYTHONPYCACHEPREFIX=build

all: init_timesone install init_db run

init_timesone:
	date

install:
	pip install -r requirements.txt

init_db:
	python3 fill_test_db.py

run:
	python3 main.py
