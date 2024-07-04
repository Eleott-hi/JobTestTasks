export PYTHONUNBUFFERED=1
export PYTHONPYCACHEPREFIX=build

all: init_timesone install init_bd run

init_timesone:
	date

install:
	pip install -r requirements.txt

wait_for_it: 
	chmod +x ./wait-for-it.sh 
	./wait-for-it.sh -t 120 "$$DB_SERVICE_HOST:$$DB_SERVICE_PORT" 

init_bd:
	python3 fill_test_db.py

run:
	python3 main.py
