# Design
API design.

# Table Of Contents
- [Overview](#overview)
- [Data Model](#data-model)
- [Endpoints](#endpoints)
  - [App Endpoints](#app-endpoints)
    - [Send Messages](#get-new-queries)
	- [New App Upload](#answer-new-queries)
  - [Meta Endpoints](#meta-endpoints)
	- [Health Check](#health-check)

# Overview
HTTP RESTful API.  

Requests pass data via JSON encoded bodies except for in GET requests where data
will be passed via URL and query parameters.

Responses will always return JSON string.

# Data Model

## UserQuery Model
`userquery` collection.


Schema:

- `user_id` (String)
- `query` (String)

## QueryData Model
`data` collection

This schema is not stored in the database, but is used to define POST request

Schema:
- `entity`
    - `entity_name` (String)
    - `sysnonyms` (List[String])
- `intent`
    - `intent_name` (String)
    - `examples` (List[String]) (The string is required to include @entity_name instead of all text. For eg. Write `What is @knative_entity_name` instead of `What is knative`)
- `node` 
    - `node_name` (String)
    - `answer`(String)

# Endpoints

The endpoints do not require authentication.  

Endpoints which specify a response of `None` will return the 
JSON: `{"ok": true}`.

## Chatbot-traing-data Endpoints
### Get new queries
`GET /newdata`

Get new questions from the chatbot-api users


Response:

- `message_resp` (Json)

### Answer new queries
`POST /newdata`

Stores meta data of new app to send it to watson for training

Request:

- `user_query` (String)  New question to be submitted to chatbot
- `query_variation` (List[String]) List of variations of same question
- `answer` (String) Answer to the given question.

Response:

- `success Message` (JsonString)


## Meta Endpoints
### Health Check
`GET /health`

Used to determine if server is operating fully.

Request: None

Response: None

