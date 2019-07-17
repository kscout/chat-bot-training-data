

DB_DATA_DIR ?= container-data/db
DB_CONTAINER_NAME ?= prod-kscout-bot-api-db
DB_USER ?= prod-kscout-bot-api
DB_PASSWORD ?= secretpassword


# Start MongoDB server in container
# Pulls docker image for latest mongo build and runs the container
db:
	mkdir -p ${DB_DATA_DIR}
	docker run \
		-it --rm --net host --name ${DB_CONTAINER_NAME} \
		-v ${PWD}/${DB_DATA_DIR}:/data/db \
		-e MONGO_INITDB_ROOT_USERNAME=${DB_USER} \
		-e MONGO_INITDB_ROOT_PASSWORD=${DB_PASSWORD} \
		mongo:latest

# Runs mongo on shell
db-cli:
	docker run -it --rm --net host mongo:latest mongo -u ${DB_USER} -p ${DB_PASSWORD}







