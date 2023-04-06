import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()

psql_password = os.environ['POSTGRES_PASSWORD']
database = 'state_migrations'

def create_connection(host_name, user_name, user_password, db_name=None):
    connection = None
    try:
        connection = psycopg2.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print('MySQL Database connection successful')
    except Exception as err:
        print(f"Error: '{err}'")
    return connection

def get_query(query):
    connection = create_connection('localhost', 'postgres', psql_password, database)
    cursor = connection.cursor()
    try:
        result = []
        cursor.execute(query)
        for row in cursor:
            result.append(row)
        cursor.close()
        return result
    except Exception as err:
        print(f"Error: '{err}'")

q_all_divisions = """
    SELECT DISTINCT s.parent_id
    FROM census_states s;
    """
    
q_states_in_div = """
    SELECT s.abbrv
    FROM census_states s
    WHERE parent_id = '{division}';
    """
    
q_migrations_to_region_from_state = """
    SELECT SUM(m.estimate)
    FROM migrations m
    WHERE m.year = {year} AND m.current_state IN (
    SELECT abbrv 
    FROM state_div_reg
    WHERE reg_id = '{state}');
    """

q_total_migration_to_region_in_year = """
    SELECT SUM(m.estimate)
	FROM migrations m
	WHERE m.year = {year} AND m.current_state IN (
	SELECT abbrv 
	FROM state_div_reg
    WHERE reg_id = '{region}');
    """
    
q_num_of_states_min_10k_moved = """
    SELECT COUNT(previous_state) {state}, year 
    FROM migrations 
    WHERE current_state='{state}' 
    AND estimate>10000
    GROUP BY year;
    """
    
q_most_moved_from_state = """
    SELECT previous_state state, migrations.year
    FROM migrations 
    INNER JOIN
	(SELECT MAX(estimate) max_est, year
	FROM migrations 
	WHERE current_state = '{state}' 
	GROUP BY year) AS m
    ON migrations.estimate = m.max_est;
    """
    
q_percent_migration = """
    SELECT m.previous_state, (m.estimate/p.population)*100 percentage, m.year
    FROM migrations m
    INNER JOIN state_pop p
    ON m.previous_state = p.state AND m.year = p.year
    WHERE current_state='{state}';
    """

# TODO: create query based on census_id, not state abbrv
q_previous_state = """
    SELECT m.current_state,
        m.previous_state, 
        m.year,
        m.estimate,
        m.estimate-m.margin_of_error,
        m.estimate+m.margin_of_error
    FROM migrations m
    WHERE current_state = 'NC'
    AND previous_state = '{state}';
    """

# TODO: refactor to append 'year' filter to prevent redundant queries (see above)
q_previous_state_year = """
    SELECT m.current_state,
        m.previous_state, 
        m.year,
        m.estimate,
        m.estimate-m.margin_of_error,
        m.estimate+m.margin_of_error
    FROM migrations m
    WHERE current_state = 'NC'
    AND previous_state = '{state}'
    AND year = '{year}';
    """

# TODO: refactor to reuse select statement (repeated 4 times)
q_previous_division = """
    SELECT 
    year,
    SUM(m.estimate),
    SUM(m.estimate)-SUM(m.margin_of_error),
    SUM(m.estimate)+SUM(m.margin_of_error)
    FROM migrations m
    WHERE m.previous_state IN (
    SELECT abbrv 
    FROM state_div_reg s
    WHERE div_id = '{division}')
    GROUP BY year;
    """

q_previous_division_year = """
    SELECT
    SUM(m.estimate) Estimate,
    SUM(m.estimate)-SUM(m.margin_of_error),
    SUM(m.estimate)+SUM(m.margin_of_error)
    FROM migrations m
    WHERE m.previous_state IN (
    SELECT abbrv 
    FROM state_div_reg s
    WHERE div_id = '{division}')
    AND year = '{year}';
    """

q_outside_south_atlantic_to_state = """
    SELECT
    year,
    SUM(m.estimate) Estimate
    FROM migrations m
    WHERE m.previous_state NOT IN (
    SELECT abbrv 
    FROM state_div_reg s
    WHERE div_id = 'D5')
    AND m.current_state = '{state}'
    GROUP BY year;
    """
    
q_all_migrations_to_state = """
    SELECT
    year,
    SUM(m.estimate) Estimate
    FROM migrations m
    WHERE m.current_state = '{state}'
    GROUP BY year;
    """
    
        
def get_all_divisions():
    return get_query(q_all_divisions)

def get_states_in_div(d):
    query = q_states_in_div.format(division=d)
    return get_query(query)

def get_migrations_to_region_from_state(y, s):
    query = q_migrations_to_region_from_state(year=y, state=s)
    return get_query(query)

def get_migration_to_region_in_year(r, y):
    query = q_total_migration_to_region_in_year.format(region=r, year=y)
    return get_query(query)

def get_num_of_states_min_10k_moved(s):
    query = q_num_of_states_min_10k_moved.format(state=s)
    return get_query(query)

def get_most_moved_from_state(s):
    query = q_most_moved_from_state.format(state=s)
    return get_query(query)

def get_percent_migration(s):
    query = q_percent_migration.format(state=s)
    return get_query(query)

def get_previous_state(s):
    query = q_previous_state.format(state=s)
    return get_query(query)

def get_previous_state_year(s, y):
    query = q_previous_state_year.format(state=s, year=y)
    return get_query(query)

def get_previous_division(d):
    query = q_previous_division.format(division=d)
    return get_query(query)

def get_previous_division_year(d, y):
    query = q_previous_division_year.format(division=d, year=y)
    return get_query(query)

def get_outside_south_atlantic_to_state(s):
    query = q_outside_south_atlantic_to_state.format(state=s)
    return get_query(query)

def get_all_migrations_to_state(s):
    query = q_all_migrations_to_state.format(state=s)
    return get_query(query)