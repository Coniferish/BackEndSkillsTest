import mysql.connector
import os

from dotenv import load_dotenv

load_dotenv()

sql_password = os.environ['MYSQL_PASSWORD']
database = 'state_migrations'

migrate_to_region_query = """
    SELECT SUM(m.estimate)
	FROM migrations m
	WHERE m.year = {} AND m.current_state IN (
	SELECT abbrv 
	FROM state_div_reg
    WHERE reg_id = '{}');
    """
    
query_states_in_region = """
    SELECT abbrv 
    FROM state_div_reg
    WHERE reg_id = '{}';
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

def get_states_in_region(region):
    query = query_states_in_region.format(region)
    return get_query(query)
