.PHONY: pip-install
pip-install:
	docker-compose run backend sh -c 'pip3 install ${package} && pip freeze > requirements.txt'
	docker-compose build

.PHONY: regen-openapi-client
regen-openapi-client:
	curl http://localhost:8000/openapi.json > openapi.json
	yarn openapi-generator generate -g typescript-axios -i http://localhost:8000/openapi.json -o ./frontend/src/client