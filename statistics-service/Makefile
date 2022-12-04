build:
	docker-compose build

run-silent:
	docker-compose up -d

run:
	docker-compose up

unit-tests:
	docker-compose -f docker-compose.test.yaml run test-statistics-api pytest api.tests
