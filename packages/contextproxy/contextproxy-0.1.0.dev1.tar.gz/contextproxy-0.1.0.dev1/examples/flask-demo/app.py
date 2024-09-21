from uuid import uuid4

from flask import Flask, current_app, jsonify, request
from flask_cors import CORS
from werkzeug.exceptions import BadRequest

from contextproxy import contextproxy

app = Flask(__name__)
CORS(app)


@app.route("/hello", methods=["GET"])
def hello():
    return "hello world"


@app.route("/echo", methods=["GET", "POST"])
def echo():
    response = request.values.copy()
    response.update(request.files)
    if request.data:
        try:
            response.update(request.get_json(force=True))
        except BadRequest:
            # Failed to decode JSON object
            response.update({"body": request.data.decode()})
    return jsonify(response)


#
# contextproxy example:
#


@contextproxy(app)
def example_resource():
    uuid = uuid4()
    current_app.logger.debug(f"before: Preparing to create example resource ({uuid})")
    try:
        current_app.logger.debug(f"yielding: Creating example resource ({uuid})")
        yield f"example resource {uuid=}"
        current_app.logger.debug(f"yielded: where is this? ({uuid})")
    except Exception as e:
        current_app.logger.debug(
            f"except: error processing example resource ({uuid}): {type(e)}: {e}"
        )
    else:
        current_app.logger.debug(f"else: okey processing example resource ({uuid})")
    finally:
        current_app.logger.debug(f"finally: Destroying example resource ({uuid})")
    current_app.logger.debug(f"after: Destroyed example resource ({uuid})")


@app.route("/resource", methods=["GET"])
def foo():
    current_app.logger.info(example_resource)
    return f"bar: {example_resource}"


if __name__ == "__main__":
    app.run(debug=True)
