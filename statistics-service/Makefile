build:
	docker-compose build

run-silent:
	docker-compose up -d

run:
	docker-compose up

tests-unit:
	docker-compose -f docker-compose.test.yaml run --user="root" --rm test-statistics-api python manage.py test api/tests/unit

tests-integration:
	docker-compose -f docker-compose.test.yaml rm -f postgres mongo
	docker-compose -f docker-compose.test.yaml up -d postgres mongo
	docker-compose -f docker-compose.test.yaml run --user="root" --rm test-statistics-api python manage.py test api/tests/int
	docker-compose -f docker-compose.test.yaml rm -f postgres mongo

tests: tests-unit | tests-integration
