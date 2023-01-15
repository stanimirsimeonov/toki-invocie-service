# List all the docker containers ran in the given application
ps:
	docker-compose ps

# run or rerun all the required services within a container
up:
	docker-compose up -d --force-recreate dynamodb dynamodb-ui postgresql zookeeper kafka kafka-ui schema-registry  schema-registry-ui minio

buckets:
	docker-compose up recreate-buckets

minio-cli:
	docker-compose run minio-cli
# get down all the infrastructure services
down:
	docker-compose down

# prune all the docker infrastructure resources
prune:
	docker system prune --all --volumes -f

pypi-install:
	pip3 install -r requirements.txt  --force-reinstall  --ignore-installed --no-cache-dir
