POSTGRES_CONTAINER_NAME := postgres_service

all: stop up

up:
	docker-compose up

stop:
	docker-compose stop

down:
	docker-compose down

logs:
	docker-compose logs

clean_db:
	-docker stop $(POSTGRES_CONTAINER_NAME)
	-docker rm   $(POSTGRES_CONTAINER_NAME)
	-rm -rf s1_service/*.db

prune:
	docker system prune -a

sed:
	find . -type f -name "*.sh" -exec sed -i 's/\r//g' {} +
