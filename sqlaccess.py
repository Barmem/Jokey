import mysql.connector

def get_records(host, user, password, database, statement, param = "", port=1881):
  # Connect to the database
  conn = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database,
    port=port
  )
  # conn.set_charset_collation('utf8_general_ci')
  # Create a cursor object
  cursor = conn.cursor()

  # Execute the SELECT statement
  if param == "":
    cursor.execute(statement)
  else:
    cursor.execute(statement, (param))
  # Fetch the records
  records = cursor.fetchall()

  # Close the cursor and connection
  cursor.close()
  conn.close()
  records = [tuple(str(x).encode('utf-8').decode('utf-8') for x in record) for record in records]
  print(records)  
  return records



# records = get_records(
#   host="localhost",
#   user="user",
#   password="password",
#   database="database",
#   statement="SELECT * FROM table WHERE column1 = 'value'"
# )
