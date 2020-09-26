.PHONY: run-stack
run-stack:
	docker-compose up

.PHONY: docker-build
docker-build:
	docker-compose build

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
	yarn install # Update the local node_modules as well
	docker-compose build

.PHONE: setup
setup:
	yarn install
	yarn --cwd frontend install
	cd ..
	touch frontend/.env
	touch backend/.env
	docker-compose build
	pre-commit install

.PHONY: lint
lint:
	pre-commit run --all-files

.PHONY: alembic-revision
alembic-revision:
	docker-compose run -w '/usr/app/app' backend sh -c 'alembic revision --auto -m "${label}"'

.PHONY: alembic-upgrade
alembic-upgrade:
	docker-compose run -w '/usr/app/app' backend sh -c 'alembic upgrade head'

.PHONY: alembic
alembic:
	docker-compose run -w '/usr/app/app' backend sh -c 'alembic ${command}'

.PHONY: test-backend
test-backend:
	docker-compose run backend sh -c 'python -m pytest tests'
