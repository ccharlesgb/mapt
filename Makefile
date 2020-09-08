.PHONY: pip-install
pip-install:
	docker-compose run backend sh -c 'pip3 install ${package} && pip freeze > requirements.txt'
	docker-compose build