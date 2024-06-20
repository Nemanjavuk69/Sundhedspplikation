import psycopg2  # Importing psycopg2 module for PostgreSQL database interaction


def conn_sql():  # Defining the function to establish a SQL connection
    dbname = 'postgres'  # or your database name  # Setting the database name
    user = 'admin'  # Setting the database user
    password = 'admin'  # Setting the database password
    host = 'localhost'  # Setting the database host
    port = '5432'  # Setting the database port
    # Establish a connection to the database
    conn = psycopg2.connect(dbname=dbname, user=user,
                            password=password, host=host, port=port)  # Connecting to the database
    cur = conn.cursor()  # Creating a cursor object
    return cur, conn  # Returning the cursor and connection


def username_exists(username):  # Defining the function to check if a username exists

    try:
        cur, conn = conn_sql()  # Getting SQL connection and cursor
        # Prepare a query to search for the username
        cur.execute("SELECT COUNT(*) FROM users WHERE username = %s",
                    # Executing the query with the provided username
                    (username.lower(),))

        # Fetch the result
        result = cur.fetchone()  # Fetching one result from the query

        # Check if the username exists
        # Returning True if the username exists, otherwise False
        return result[0] > 0

    except psycopg2.Error as e:  # Handling database errors
        print(f"Database error: {e}")  # Printing the error message
        return False  # Returning False in case of an error

    finally:
        if cur is not None:  # Checking if cursor is not None
            cur.close()  # Closing the cursor
        if conn is not None:  # Checking if connection is not None
            conn.close()  # Closing the connection


def email_exists(email):  # Defining the function to check if an email exists

    try:
        cur, conn = conn_sql()  # Getting SQL connection and cursor

        # Prepare a query to search for the username
        cur.execute("SELECT COUNT(*) FROM users WHERE email = %s",
                    (email.lower(),))  # Executing the query with the provided email

        # Fetch the result
        result_P = cur.fetchone()  # Fetching one result from the query

        # Prepare a query to search for the username
        cur.execute("SELECT COUNT(*) FROM doctors WHERE email = %s",
                    (email.lower(),))  # Executing the query with the provided email

        # Fetch the result
        result_D = cur.fetchone()  # Fetching one result from the query

        # Check if the username exists
        # Returning True if the email exists in either table, otherwise False
        return result_P[0] > 0 or result_D[0] > 0

    except psycopg2.Error as e:  # Handling database errors
        print(f"Database error: {e}")  # Printing the error message
        return False  # Returning False in case of an error

    finally:
        if cur is not None:  # Checking if cursor is not None
            cur.close()  # Closing the cursor
        if conn is not None:  # Checking if connection is not None
            conn.close()  # Closing the connection
