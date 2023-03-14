from flask import Flask, jsonify, make_response
from .db import *
import pandas as pd
from io import StringIO
import csv
from collections import defaultdict

app = Flask(__name__)

def get_csv(df, file_name):
    # https://stackoverflow.com/questions/56007695/download-csv-file-in-flask-best-practice
    sio = StringIO()
    writer = csv.writer(sio)
    writer.writerow(df.columns.tolist())
    writer.writerows(df.values.tolist())
    output = make_response(sio.getvalue())
    output.headers['Content-Disposition'] = f'attachment; filename={file_name}.csv'
    output.headers['Content-type'] = 'text/csv'
    return output

@app.route('/migrationto/<region>/<year>/')
def migration_to_region_in_year(region, year):
    response = jsonify(get_migration_to_region_in_year(region, year))
    return response

# @app.route('/q1/')
# def q1():
#     # get all states in a division (note the region they're in)
#     divisions =  get_all_divisions
#     div_states = {division: [get_states_in_div] for division in divisions}
#     # for each state:
#     for div, states in div_states:
#         for state in states:
#             for year in range(2010,2020):
#                 sum_migrations = get_migrations_to_region_from_state()
#         # sum += estimate (of each region)
#     pass
    

@app.route('/q2/<state>/')
def q2(state):
    count_10k = get_num_of_states_min_10k_moved(state)
    count_10k_df = pd.DataFrame(count_10k, columns=['Count of States with Migration > 10k', 'Year'])
    
    most_moved = get_most_moved_from_state(state)
    most_moved_df = pd.DataFrame(most_moved, columns=['State with Highest Total Migration', 'Year'])
    
    percent_migration = get_percent_migration(state)
    percent_migration_df = pd.DataFrame(percent_migration, columns=['State with Highest Migration Proportion', 'Percent Migrated', 'Year'])
    idx = percent_migration_df.groupby(['Year'])['Percent Migrated'].transform(max) == percent_migration_df['Percent Migrated']   
    
    dfs = pd.merge(most_moved_df, count_10k_df, how='outer', on='Year')
    dfs = pd.merge(percent_migration_df[idx], dfs, how='outer', on='Year')
    file_name = f"{state}_migration_stats"
    return get_csv(dfs, file_name)

# TODO: create query based on census_id, not state abbrv
@app.route('/previous_state/<id>/', defaults={'year':None})
@app.route('/previous_state/<id>/<year>/')
def previous_state(id, year):
    # https://flask.palletsprojects.com/en/2.2.x/api/#url-route-registrations
    columns=['Current State', 'Previous State', 'Year', 'Estimated Migration', 'Estiamted Migration LB', 'Estimated Migration UB']
    if year:
        response = pd.DataFrame(get_previous_state_year(id, year), columns=columns)
    else:
        response = pd.DataFrame(get_previous_state(id), columns=columns)
    return response.to_json()

@app.route('/previous_division/<id>/', defaults={'year':None})
@app.route('/previous_division/<id>/<year>/')
def previous_division(id, year):
    columns=['Division', 'Year', 'Estimated Migration', 'Estiamted Migration LB', 'Estimated Migration UB']
    # current_state = NC, so sum of the states that moved to N (by division)
    if year:
        response = get_previous_division_year(id, year)
        response = pd.DataFrame(
            [(id, year)+row for row in response], 
            columns=columns
            )
    else:
        response = get_previous_division(id)
        response = pd.DataFrame(
            [(id,)+row for row in response],
            columns=columns
            )
    return response.to_json()

if __name__ == '__main__':
    app.run(debug=True)
    