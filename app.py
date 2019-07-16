from flask import Flask, Response, request
from flask_cors import CORS, cross_origin
from processrequest import get_user_queries, add_query_answers
import json

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
        api_response = get_user_queries()
        return Response(json.dumps(api_response), status=400, mimetype='application/json')



@app.route('/health', methods=['GET', 'POST'])
# @disable_logging
def health_probe() -> Response:
    status = dict()
    status["ok"] = True
    return Response(json.dumps(status), status=200, mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
