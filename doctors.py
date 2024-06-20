import csv  # Importing the CSV module
from flask import session  # Importing session from Flask
# Importing the SQL connection function from lookupSQL
from lookupSQL import conn_sql
from psycopg2 import sql  # Importing the SQL module from psycopg2


# Defining the function to verify doctor credentials
def verify_doctor_credentials(username, password):

    try:
        cur, conn = conn_sql()  # Getting SQL connection and cursor

        # Execute the query to verify doctor credentials
        query = sql.SQL(
            # SQL query to verify credentials
            "SELECT id, email FROM your_table_name WHERE username = %s AND password = %s")
        # Executing the query with provided username and password
        cur.execute(query, (username, password))

        # Fetch the result
        result = cur.fetchone()  # Fetching one result from the query

        # Close the cursor and connection
        cur.close()  # Closing the cursor
        conn.close()  # Closing the connection

        if result:  # Checking if result is not None
            # Returning True, email, and ID if credentials are valid
            return True, result[1], result[0]
        else:
            return False, None, None  # Returning False, None, None if credentials are invalid

    except Exception as e:  # Handling exceptions
        print(f"An error occurred: {e}")  # Printing the error message
        return False, None, None  # Returning False, None, None in case of an error
