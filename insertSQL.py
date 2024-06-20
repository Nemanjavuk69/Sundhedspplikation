import psycopg2  # Importing the psycopg2 module for PostgreSQL database interaction
# Importing the SQL connection function from lookupSQL
from lookupSQL import conn_sql


# Defining the function to insert a new user into the database
def postgreSQL_con(new_user, user_password, user_email, user_type):

    try:
        cur, conn = conn_sql()  # Getting SQL connection and cursor

        if user_type == 'P':  # Checking if the user type is 'P' (patient)
            # Find the maximum ID and add 1 for the new user's ID
            # SQL query to get the next ID for a new user
            cur.execute("SELECT COALESCE(MAX(id), 0) + 1 FROM users;")
            new_id = cur.fetchone()[0]  # Fetching the new ID

            # SQL for inserting a new user
            # SQL query to insert a new user
            insert_sql = "INSERT INTO users (Username, Password, Email, ID, Type) VALUES (%s, %s, %s, %s, %s);"
            user_data = (new_user, user_password, user_email,
                         new_id, user_type)  # Data for the new user

            # Execute the insert SQL with data
            # Executing the insert query with user data
            cur.execute(insert_sql, user_data)
            conn.commit()  # Committing the transaction
        else:  # If the user type is not 'P' (assumed to be 'D' for doctor)
            # Find the maximum ID and add 1 for the new user's ID
            # SQL query to get the next ID for a new doctor
            cur.execute("SELECT COALESCE(MAX(id), 0) + 1 FROM doctors;")
            new_id = cur.fetchone()[0]  # Fetching the new ID

            # SQL for inserting a new user
            # SQL query to insert a new doctor
            insert_sql = "INSERT INTO doctors (Username, Password, Email, ID, Type) VALUES (%s, %s, %s, %s, %s);"
            user_data = (new_user, user_password, user_email,
                         new_id, user_type)  # Data for the new doctor

            # Execute the insert SQL with data
            # Executing the insert query with doctor data
            cur.execute(insert_sql, user_data)
            conn.commit()  # Committing the transaction

    except psycopg2.Error as e:  # Handling database errors
        print(f"Database error: {e}")  # Printing the error message
        conn.rollback()  # Rolling back the transaction

    finally:  # Ensuring resources are closed properly
        if cur is not None:  # Checking if cursor is not None
            cur.close()  # Closing the cursor
        if conn is not None:  # Checking if connection is not None
            conn.close()  # Closing the connection
