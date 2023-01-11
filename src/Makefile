install:
	pip install -r requirements.txt

test:
	ENVIRONMENT=local python3 -c 'from handlers.camara_news.insert import handler; handler("", "")'

docker: 
	docker build --platform linux/amd64 -t scrapper:latest .
	docker run -p 9000:8080 --platform linux/amd64 scrapper:latest handlers/camara_news/insert.handler

signal:
	curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}'
