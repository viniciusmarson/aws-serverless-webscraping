install:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

run:
	ENVIRONMENT=local python3 -m handlers.$(handler).$(file)

test:
	pytest

docker-build: 
	docker build --platform linux/amd64 -t scrapper:latest .

docker-run: 
	docker run -p 9000:8080 --platform linux/amd64 scrapper:latest handlers/$(handler)/$(file).handler

signal:
	curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}'
