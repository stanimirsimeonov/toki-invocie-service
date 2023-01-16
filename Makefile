current_dir :=  $(shell pwd)

# List all the docker containers ran in the given application
ps:
	docker-compose ps

# run or rerun all the required services within a container
up:
	docker-compose up -d --force-recreate dynamodb dynamodb-ui postgresql zookeeper kafka kafka-ui schema-registry  schema-registry-ui minio

buckets:
	docker-compose up recreate-buckets

venv:
	python -m venv venv

venv-activate:


minio-cli:
	docker-compose run minio-cli
# get down all the infrastructure services
down:
	docker-compose down

# prune all the docker infrastructure resources
prune:
	docker system prune --all --volumes -f

pypi-install:
	pip install -r ./src/requirements.txt  --force-reinstall  --ignore-installed --no-cache-dir

install:
	cd src && pip install .  --force-reinstall  --ignore-installed --no-cache-dir

run:
	export SIMPLE_SETTINGS=settings;
	cd src && python -m toki -l info --datadir=../data/toki-workers-data --debug worker --web-port=6000

prices:
	export SIMPLE_SETTINGS=settings;
	cd src && python -m toki scrape-exchanges --from-date 2022-01-01