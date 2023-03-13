from flask import Flask, jsonify
# from .db import get_states_in_region, get_migration_to_region_in_year
from .db import *

app = Flask(__name__)

@app.route('/statesin/<region>')
def states_in_region(region):
    response = jsonify(get_states_in_region(region))
    return response

@app.route('/migrationto/<region>/<year>')
def migration_to_region_in_year(region, year):
    response = jsonify(get_migration_to_region_in_year(region, year))
    return response

if __name__ == '__main__':
    app.run(debug=True)
