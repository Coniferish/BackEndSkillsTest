from flask import Flask, jsonify, make_response
from .db import *
import pandas as pd
from io import StringIO
import csv
from collections import defaultdict

app = Flask(__name__)

def write_csv(data, file_name):
    # https://stackoverflow.com/questions/56007695/download-csv-file-in-flask-best-practice
    sio = StringIO()
    writer = csv.writer(sio)
    if type(data) == pd.DataFrame:
        writer.writerow(data.columns.tolist())
        writer.writerows(data.values.tolist())
    elif type(data) == defaultdict:
        fields = ['Division to Region per Year', 'Estimate']
        writer.writerow(fields)
        for item in data.items():
            writer.writerow(item)
    else:
        return 'Error writing csv'
    output = make_response(sio.getvalue())
    output.headers['Content-Disposition'] = f'attachment; filename={file_name}.csv'
    output.headers['Content-type'] = 'text/csv'
    return output

@app.route('/')
def home():
    routes = """Routes: <br/>
    /task1/ <br/>
    /task2/[state: two-letter abbreviation]/ <br/>
    /previous_state/[id]/ <br/>
    /previous_state/[id]/[year]/ <br/>
    /previous_division/[id]/ <br/>
    /previous_division/[id]/[year]/
    /migrationto/[region]/[year]/ <br/>"""
    return routes

@app.route('/migrationto/<region>/<year>/')
def migration_to_region_in_year(region, year):
    response = jsonify(get_migration_to_region_in_year(region, year))
    return response

@app.route('/task1/')
def q1():    
    divisions_to_regions = defaultdict(lambda: 0)    
    state_to_div = {}
    div_to_region = {}
    states_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data/census_states.csv')
    divs_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data/regions_and_divisions.csv')
    
    # Lazy creation of a dict containing divisions and the regions they belong to.
    # It does not account for column headers or regions (which don't have a parent_id).
    # Instead of having two very similar scripts, I could define a function, but then
    # I would have to account for the column indices differences for what I'm looking for.
    # I also am choosing to use state abbreviations 
    # later below because those are what's used in the migrations.csv file.
    with open(divs_file_path) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            div_to_region[row[0]] = row[-1]
    
    with open(states_file_path) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            state_to_div[row[2]] = row[-1]
    
    migrations_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data/migrations.csv')
    
    with open(migrations_file_path) as csvfile:
        next(csvfile)
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            current_state = row[0]
            previous_state = row[1]
            estimate = row[2]
            year = row[4]
            # data was not fully cleaned to remove PR (which isn't listed in divisions or regions)
            if current_state == 'PR':
                continue
            curr_region = div_to_region[state_to_div[current_state]]
            prev_div = state_to_div[previous_state]
            
            divisions_to_regions[prev_div + ' to ' + curr_region + ' ' + year] += int(estimate)
            
    file_name = 'division_to_region_migration_stats'
    return write_csv(divisions_to_regions, file_name)
    

@app.route('/task2/<state>/')
def q2(state):
    count_10k = get_num_of_states_min_10k_moved(state)
    count_10k_df = pd.DataFrame(count_10k, columns=['Count of States with Migration > 10k', 'Year'])
    
    most_moved = get_most_moved_from_state(state)
    most_moved_df = pd.DataFrame(most_moved, columns=['State with Highest Total Migration', 'Year'])
    
    outside_south_atlantic = get_outside_south_atlantic_to_state(state)
    migration_outside_south_atlantic = pd.DataFrame(outside_south_atlantic, columns=['Year', 'Estimate D5'])
    
    all_migrations_to_state = get_all_migrations_to_state(state)
    all_migrations = pd.DataFrame(all_migrations_to_state, columns=['Year', 'Estimate Total'])
    
    percent_s_a = pd.merge(all_migrations, migration_outside_south_atlantic, how='outer', on='Year')
    percent_s_a['Percent Migrations from Outside South Atlantic'] = percent_s_a['Estimate D5']/percent_s_a['Estimate Total']*100
    percent_s_a.drop(['Estimate D5', 'Estimate Total'], inplace=True, axis=1)
    
    percent_migration = get_percent_migration(state)
    percent_migration_df = pd.DataFrame(percent_migration, columns=[
        'State with Highest Migration Proportion', 
        'Percent Migration from State with Highest Proportion', 
        'Year'])
    idx = percent_migration_df.groupby(['Year'])['Percent Migration from State with Highest Proportion'].transform(max) == percent_migration_df['Percent Migration from State with Highest Proportion']   
    
    df = pd.merge(most_moved_df, count_10k_df, how='outer', on='Year')
    df = pd.merge(percent_migration_df[idx], df, how='outer', on='Year')
    df = pd.merge(percent_s_a, df, how='outer', on='Year')
    # https://stackoverflow.com/questions/53141240/pandas-how-to-swap-or-reorder-columns
    cols = list(df.columns)
    a = cols.index('Year')
    cols = [cols[a]] + cols[:a] + cols[a+1:]
    file_name = f"{state}_migration_stats"
    df = df[cols]
    return write_csv(df, file_name)

# TODO: create query based on census_id, not state abbrv
@app.route('/previous_state/<id>/', defaults={'year':None})
@app.route('/previous_state/<id>/<year>/')
def previous_state(id, year):
    # https://flask.palletsprojects.com/en/2.2.x/api/#url-route-registrations
    columns=['Current State', 
             'Previous State', 
             'Year', 
             'Estimated Migration', 
             'Estiamted Migration LB', 
             'Estimated Migration UB']
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
    