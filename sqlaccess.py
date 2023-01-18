import mysql.connector
from main import args 
def get_records(statement, port=1881):
  # Connect to the database
  conn = mysql.connector.connect(
    args.host,
    args.user,
    args.password,
    args.database,
    port=port
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
  print(records)  
  return records

def insert_records(query, port=1881): 
  try: 
    db_con = mysql.connector.connect(
      main.args.host,
      main.args.user,
      main.args.password,
      main.args.database,
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
