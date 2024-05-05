all: init_timesone install wait_for_it run

init_timesone:
	date

install:
	pip install -r requirements.txt

wait_for_it: 
	chmod +x ./wait-for-it.sh 
	./wait-for-it.sh -t 120 postgres_service:5432

run: migrations  loaddata 
	python manage.py runserver 0.0.0.0:8000

migrations:
	python manage.py makemigrations menu
	python manage.py migrate

superuser:	
	python manage.py createsuperuser --no-input

init:
	python3 manage.py startapp menu

loaddata:
	python manage.py loaddata menu_items.json