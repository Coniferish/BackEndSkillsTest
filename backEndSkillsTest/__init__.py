from flask import Flask, jsonify
# from .db import get_states_in_region, get_migration_to_region_in_year
from .db import *
import pandas as pd

app = Flask(__name__)

@app.route('/statesin/<region>/')
def states_in_region(region):
    response = jsonify(get_states_in_region(region))
    return response

@app.route('/migrationto/<region>/<year>/')
def migration_to_region_in_year(region, year):
    response = jsonify(get_migration_to_region_in_year(region, year))
    return response

@app.route('/min10k/<state>/')
def num_of_states_min_10k_moved(state):
    response = jsonify(get_num_of_states_min_10k_moved(state))
    return response

@app.route('/q2/<state>/')
def q2(state):
    # hard-coded because not all subqueries for this view support substitution
    # state = 'nc'
    count_10k = get_num_of_states_min_10k_moved(state.upper())
    count_10k_df = pd.DataFrame(count_10k, columns=['Count of States with Migration > 10k', 'Year'])
    
    most_moved = get_most_moved_from_state(state.upper())
    most_moved_df = pd.DataFrame(most_moved, columns=['State with Highest Total Migration', 'Year'])
    
    percent_migration = get_percent_migration(state.upper())
    percent_migration_df = pd.DataFrame(percent_migration, columns=['State with Highest Migration Proportion', 'Percent Migrated', 'Year'])
    idx = percent_migration_df.groupby(['Year'])['Percent Migrated'].transform(max) == percent_migration_df['Percent Migrated']   
    
    dfs = pd.merge(most_moved_df, count_10k_df, how='outer', on='Year')
    dfs = pd.merge(percent_migration_df[idx], dfs, how='outer', on='Year')
    print(dfs)
    return dfs.to_json()

# TODO: create query based on census_id, not state abbrv
@app.route('/previous_state/<id>/', defaults={'year':None})
@app.route('/previous_state/<id>/<year>/')
def previous_state(id, year):
    # https://flask.palletsprojects.com/en/2.2.x/api/#url-route-registrations
    if year:
        response = get_previous_state_year(id, year)
    else:
        response = get_previous_state(id)
    
    return response

if __name__ == '__main__':
    app.run(debug=True)
    