import mysql.connector
import os

from dotenv import load_dotenv

load_dotenv()

sql_password = os.environ['MYSQL_PASSWORD']
database = 'state_migrations'

q_total_migration_to_region_in_year = """
    SELECT SUM(m.estimate)
	FROM migrations m
	WHERE m.year = {year} AND m.current_state IN (
	SELECT abbrv 
	FROM state_div_reg
    WHERE reg_id = '{region}');
    """
    
q_states_in_region = """
    SELECT abbrv 
    FROM state_div_reg
    WHERE reg_id = '{region}';
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

def create_connection(host_name, user_name, user_password, db_name=None):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Exception as err:
        print(f"Error: '{err}'")
    return connection

def get_query(query):
    connection = create_connection("localhost", "root", sql_password, database)
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

def get_states_in_region(r):
    query = q_states_in_region.format(region=r)
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
