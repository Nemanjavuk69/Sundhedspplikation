# Importing the SQL connection function from lookupSQL
from lookupSQL import conn_sql
from psycopg2 import sql  # Importing the SQL module from psycopg2


# Defining the function to get health journal entries for a user
def get_health_journal(user_id):
    user_id = str(user_id)  # Ensure user_id is a string
    entries = []  # Initializing an empty list to store journal entries

    try:
        # Connect to the PostgreSQL database
        cur, conn = conn_sql()  # Getting SQL connection and cursor

        # Execute the query to fetch entries for the given user_id
        # SQL query to select entries for the user
        query = sql.SQL("SELECT Entry FROM journals WHERE UserID = %s")
        # Executing the query with the provided user_id
        cur.execute(query, [user_id])

        # Fetch all matching entries
        rows = cur.fetchall()  # Fetching all rows from the query result
        for row in rows:  # Iterating through the rows
            # Assuming Entry is the first column in the result
            entries.append(row[0])  # Appending the entry to the list

        # Close the cursor and connection
        cur.close()  # Closing the cursor
        conn.close()  # Closing the connection

    except Exception as e:  # Handling exceptions
        print(f"An error occurred: {e}")  # Printing the error message

    return entries  # Returning the list of entries
