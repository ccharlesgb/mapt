.PHONY: pip-install
pip-install:
	docker-compose run backend sh -c 'pip3 install ${package} && pip freeze > requirements.txt'
	docker-compose build

.PHONY: regen-openapi-client
regen-openapi-client:
	curl http://localhost:8000/openapi.json > openapi.json
	yarn openapi-generator generate -g typescript-axios -i http://localhost:8000/openapi.json -o ./frontend/src/client

.PHONY: yarn-add
yarn-add:
	docker-compose run frontend sh -c 'yarn add ${package}'
	docker-compose build

.PHONY: run-stack
run-stack:
	docker-compose up

.PHONE: test-frontend
test-frontend:
