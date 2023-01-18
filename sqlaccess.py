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
  print(records)  
  return records

def insert_records(host, user, password, database, query, port=1881): 
  try: 
    db_con = mysql.connector.connect(
      host=host,
      user=user,
      password=password,
      database=database,
      port=port
    ) 
    print(query)
    cursor  = db_con.cursor()
    cursor.execute(query) 
    db_con.commit() 
    print("Query executed successfully!") 
  except mysql.connector.Error as e: 
    print(f"The error '{e}' occurred") 



# records = get_records(
#   host="localhost",
#   user="user",
#   password="password",
#   database="database",
#   statement="SELECT * FROM table WHERE column1 = 'value'"
# )
