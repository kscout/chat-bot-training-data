from config.config import service
from config.logger import logger
import os
from pymongo import MongoClient
from config import config

# Connecting to MondoDB
client = MongoClient(config.db_config["DB_HOST"], config.db_config["DB_PORT"], username=config.db_config["DB_USER"],
                     password=config.db_config["DB_PASSWORD"], connect=False)  # Connection to MongoDB
database = config.db_config["DB_NAME"]
userQuery = config.db_config["USER_QUERY"]

db_query = client[database][userQuery]


def get_user_queries():
    try:
        response = db_query.find()
        resp = []
        for i in response:
            resp.append({"user_id": i['user_id'], "queries": i['message']})
        response = {"entries": resp}
        logger.info("All queries fetched")
    except Exception as e:
        raise Exception({"error": str(e)})

    try:
        db_query.drop()
        logger.info("All queries deleted")
    except Exception as e:
        raise Exception({"error": str(e)})

    return response


# function to create new topic in chatbot
def create_query_entity(request_data):
    # create entity
    try:
        synonym_values = []
        for i in range(len(request_data['entity']['synonyms'])):
            synonym_values.append({'value': request_data['entity']['synonyms'][i]})

        response = service.create_entity(
            workspace_id=os.environ['WORKSPACE_ID'],
            entity=request_data['entity']['entity_name'],
            values=synonym_values
        ).get_result()

        return {"message": "Entity created successfully " + str(response)}
    except Exception as e:
        raise Exception({"error": "Entity already exists or error in creation" + str(e)})


# function to create questions and their variations
def create_query_intent(request_data):
    # create intent
    try:
        example_values = []
        for i in range(len(request_data['intent']['examples'])):
            example_values.append({'text': request_data['intent']['examples'][i]})
        response = service.create_intent(
            workspace_id=os.environ['WORKSPACE_ID'],
            intent=request_data['intent']['intent_name'],
            examples=example_values).get_result()
        return {"message": "Intent created successfully" + str(response)}
    except Exception as e:
        raise Exception({"error": "Intent already exists or error in creation " + str(e)})


# function to create dialogue node with answer
def create_query_node(request_data):
    try:
        response = service.create_dialog_node(
            workspace_id=os.environ['WORKSPACE_ID'],
            dialog_node=request_data['node']['node_name'],
            conditions='(#' + str(request_data['intent']['intent_name'])+' || @'+str(request_data['entity']['entity_name'])+') && intents[0].confidence > 0.8',
            previous_sibling="Welcome",
            output={
                "generic": [
                    {
                        "values": [
                            {
                                "text": request_data['node']['answer']
                            }
                        ],
                        "response_type": "text",
                        "selection_policy": "sequential"
                    }
                ]
            }
        ).get_result()
        return {"message": "Dialogue node created successfully" + str(response)}
    except Exception as e:
        raise Exception({"error": "Dialogue node already exists or error in creation " + str(e)})


def add_query_answers(request_data):
    try:
        for i in range(len(request_data['data'])):
            # Create new entity (topic) in chatbot
            new_entity = create_query_entity(request_data['data'][i])
            logger.info(new_entity)

            # Create new intent (questions) related to the entity
            new_intent = create_query_intent(request_data['data'][i])
            logger.info(new_intent)

            # Create dialogue node, which will provide answer
            new_node = create_query_node(request_data['data'][i])
            logger.info(new_node)

        return {"message": "Data source updated"}

    except Exception as e:
        raise Exception({"error": "Failed to update data source" + str(e)})
