run-infra:
	docker-compose up -d

run-services:
	cd news-service && make run-silent
	cd statistics-service && make run-silent
	cd kin-news-frontend && make run-silent

run: | run-infra run-services
