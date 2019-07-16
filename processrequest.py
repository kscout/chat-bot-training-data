from config.config import service
from config.logger import logger
import os


def get_user_queries():
    return


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
            conditions='#' + str(request_data['intent']['intent_name']),
            parent="node_1_1560874446552",
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


# function to update parent node condition to identify newly created dialogue node
def update_learning_node(request_data):
    # node_id can be acquired only by downloading the skill data
    try:
        response = service.get_dialog_node(
            workspace_id=os.environ['WORKSPACE_ID'],
            dialog_node='node_1_1560874446552'
        ).get_result()

        update_conditions = "#" + str(request_data['intent']['intent_name']) + " || " + response["conditions"]

        print(update_conditions)

        response = service.update_dialog_node(
            workspace_id=os.environ['WORKSPACE_ID'],
            dialog_node='node_1_1560874446552',
            new_conditions=update_conditions
        ).get_result()
        return {"message": "Updated parent node created successfully" + str(response)}
    except Exception as e:
        raise Exception({"error": "Updated parent node already exists or error in creation " + str(e)})


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

            # Update parent node to identify newly added dialogue node
            updated_parent = update_learning_node(request_data['data'][i])
            logger.info(updated_parent)

        return {"message": "Data source updated"}

    except Exception as e:
        raise Exception({"error": "Failed to update data source" + str(e)})
