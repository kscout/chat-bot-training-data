from config.config import service
import os

def get_user_queries():
    return

def add_query_answers(request_data):
    request_data = request_data["data"][0]

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

        print(response)
    except:
        print("Entity already exists or error in creation")

    # create intent
    try:
        example_values = []
        for i in range(len(request_data['intent']['examples'])):
            example_values.append({'text': request_data['intent']['examples'][i]})
        print(example_values)
        response = service.create_intent(
            workspace_id=os.environ['WORKSPACE_ID'],
            intent=request_data['intent']['intent_name'],
            examples=example_values).get_result()
        print(response)
    except Exception as e:
        print("Intent already exists or error in creation " + str(e))


    # create node
    # update condition
    return {"message":"Entity created"}