from flask import Flask, jsonify
# from .db import get_states_in_region, get_migration_to_region_in_year
from .db import *
import pandas as pd

app = Flask(__name__)

@app.route('/statesin/<region>')
def states_in_region(region):
    response = jsonify(get_states_in_region(region))
    return response

@app.route('/migrationto/<region>/<year>')
def migration_to_region_in_year(region, year):
    response = jsonify(get_migration_to_region_in_year(region, year))
    return response

@app.route('/min10k/<state>')
def num_of_states_min_10k_moved(state):
    response = jsonify(get_num_of_states_min_10k_moved(state))
    return response

@app.route('/q2/<state>')
def q2(state):
    count_10k = get_num_of_states_min_10k_moved(state)
    count_df = pd.DataFrame(count_10k, columns=['Count', 'Year'])
    print(count_df)
    return count_10k

if __name__ == '__main__':
    app.run(debug=True)
