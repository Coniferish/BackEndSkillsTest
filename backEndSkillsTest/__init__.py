from flask import Flask, jsonify
from .db import get_states_in_region

app = Flask(__name__)

@app.route('/statesin/<region>')
def states_in_region(region):
    response = jsonify(get_states_in_region(region))
    return response

if __name__ == '__main__':
    app.run(debug=True)
