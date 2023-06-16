import psycopg2
import config


# Establish the connection
try:
    connection = psycopg2.connect(
        host=config.host,
        port=config.port,
        database=config.database,
        user=config.user,
        password=config.password
    )
    cursor = connection.cursor()
    print('Connected to the PostgreSQL database successfully!')

    # Execute database operations here

except (Exception, psycopg2.Error) as error:
    print('Error while connecting to the PostgreSQL database:', error)
finally:
    # Close the cursor and connection
    if connection:
        cursor.close()
        connection.close()
        print('PostgreSQL connection is closed')