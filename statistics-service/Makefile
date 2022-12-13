build:
	docker-compose build

run-silent:
	docker-compose up -d

run:
	docker-compose up

tests:
	docker-compose -f docker-compose.test.yaml rm -fa postgres
	docker-compose -f docker-compose.test.yaml up -d postgres
	docker-compose -f docker-compose.test.yaml run --user="root" --rm test-statistics-api python manage.py test
	docker-compose stop
	docker-compose -f docker-compose.test.yaml rm -fa postgres
