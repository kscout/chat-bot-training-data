from flask import Flask, Response, request
from flask_cors import CORS, cross_origin
from processrequest import get_user_queries, add_query_answers
from pymongo import MongoClient
from config import config
import json
from config.logger import logger


# Connecting to MondoDB
client = MongoClient(config.db_config["DB_HOST"], config.db_config["DB_PORT"], username=config.db_config["DB_USER"],
                     password=config.db_config["DB_PASSWORD"], connect=False)  # Connection to MongoDB
database = config.db_config["DB_NAME"]
userQuery = config.db_config["USER_QUERY"]

db_query = client[database][userQuery]


logger.info("Connection to Database: " + str(db_query))
if db_query.insert_one({'user_id': ["xxx_xxx_xxx_xxx_test"]}).inserted_id:
    try:
        db_query.delete_many({'user_id': ["xxx_xxx_xxx_xxx_test"]})
        logger.info("Connection to Database Successful")

    except Exception as e:
        logger.info("Error Connecting to Database: " + str(e))

else:
    logger.info("Error Connecting to Database")


app = Flask(__name__)
CORS(app)


# Function to receive messages from client application
@app.route('/newdata', methods=['GET', 'POST'])
@cross_origin()
def receive_messages():
    if request.method == 'POST':
        try:
            request_data = add_query_answers(request.get_json())

            return Response(json.dumps(request_data), status=200, mimetype='application/json')
        except IndexError:
            status = {"error": "Index Error"}
            return Response(json.dumps(status), status=400, mimetype='application/json')
        except Exception as e:
            status = {"error": str(e)}
            return Response(json.dumps(status), status=400, mimetype='application/json')

    else:
        try:
            request_data = get_user_queries()

            return Response(json.dumps(request_data), status=200, mimetype='application/json')
        except IndexError:
            status = {"error": "Index Error"}
            return Response(json.dumps(status), status=400, mimetype='application/json')
        except Exception as e:
            status = {"error": str(e)}
            return Response(json.dumps(status), status=400, mimetype='application/json')



@app.route('/health', methods=['GET', 'POST'])
# @disable_logging
def health_probe() -> Response:
    status = dict()
    status["ok"] = True
    return Response(json.dumps(status), status=200, mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
