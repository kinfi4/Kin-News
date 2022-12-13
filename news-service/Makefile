build:
	docker-compose build

run-silent:
	docker-compose up -d

run:
	docker-compose up

tests:
	docker-compose -f docker-compose.test.yaml rm -f postgres redis
	docker-compose -f docker-compose.test.yaml up -d postgres redis
	docker-compose -f docker-compose.test.yaml run --user="root" --rm test-api python manage.py test
	docker-compose -f docker-compose.test.yaml rm -f postgres redis