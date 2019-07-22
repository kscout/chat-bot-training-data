# Chatbot Training Data
API which manages user logs and adds new queries and their answers to chatbot-api


## Table Of Contents
- [Overview](#overview)
- [Development](#development)
- [Deployment](#deployment)

## Overview
HTTP RESTful API.

Requests pass data via JSON encoded bodies except for in GET requests where data will be passed via URL and query parameters.

Responses will always return JSON String.




## Development
The Chatbot-training-data server can be run locally. Visit [DESIGN.md](DESIGN.md) to see all endpoints and corresponding responses.

Follow the steps in the [Database](#database), [Configuration](#configuration),
and [Run](#run) sections.

### Database
Start a local MongoDB server by running:

```
make db

```

### Configuration


Configuration is passed via environment variables.
- `API_KEY` : API key assigned to the bot
- `WORKSPACE_ID` :Unique id given to the created skill
- `APP_DB_HOST` : Database host
- `APP_DB_NAME` : Database name
- `APP_DB_USER` : User for this database
- `APP_DB_PASSWORD` : Database user password


## Deployment
### Deployment Configuration
Create a copy of `deploy/values.secrets.example.yaml` named 
`deploy/values.secrets.ENV.yaml` for whichever deployment environment you wish
to configure.

Edit this file with your own values.

Never commit this file.

### Deploy
Initialize submodules:

```
git submodule update --init --recursive
```

Deploy production by running:

```
make deploy-prod
```

If this is the first time production has been deployed run:

```
make rollout-prod
```

## Access 

In order to access the ChatBot Training Data, you need to be logged in to the cluster from your terminal. 

To access the API on local machine, Start thr proxy to the cluster, use command:
```
make proxy
```

In order to check if the proxy is running and cluster can e accessed, use:
```
make get-health
```

To access API, call the URL on the browser or Postman :
```
http://localhost:8001/api/v1/namespaces/kscout/services/${ENV}-${APP}":http/proxy/<ENDPOINT>
``` 
