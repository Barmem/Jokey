import mysql.connector

def get_records(host, user, password, database, statement):
  # Connect to the database
  conn = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database
  )

  # Create a cursor object
  cursor = conn.cursor()

  # Execute the SELECT statement
  cursor.execute(statement)

  # Fetch the records
  records = cursor.fetchall()

  # Close the cursor and connection
  cursor.close()
  conn.close()

  return records



# records = get_records(
#   host="localhost",
#   user="user",
#   password="password",
#   database="database",
#   statement="SELECT * FROM table WHERE column1 = 'value'"
# )
