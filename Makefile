# List all the docker containers ran in the given application
ps:
	docker-compose ps

# run or rerun all the required services within a container
up:
	docker-compose up -d --force-recreate

# get down all the infrastructure services
down:
	docker-compose down

# prune all the docker infrastructure resources
prune:
	docker system prune --all --volumes -f