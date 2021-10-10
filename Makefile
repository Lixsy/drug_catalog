build:
	docker-compose build

run:
	docker-compose up

test:
	./pytest_run.sh

execute:
	docker-compose exec drug_catalog sh

import:
	 docker-compose exec drug_catalog python import_drugs.py
