# coding=utf-8
import mysql.connector
from main import args, updaterRegister 
def get_records(statement, port=args.port):
  # Connect to the database
  # print(f"{args.host}, {args.user}, {args.password}, {args.database}")
  conn = mysql.connector.connect(
    host=args.host,
    user=args.user,
    password=args.password,
    database=args.database,
    port=port
  )

  # Create a cursor object
  cursor = conn.cursor()

  # Execute the SELECT statement
  cursor.execute(statement, "")
  # Fetch the records
  records = cursor.fetchall()

  # Close the cursor and connection
  cursor.close()
  conn.close()
  # print(records)  
  return records

def insert_records(query, port=args.port): 
  try: 
    db_con = mysql.connector.connect(
      host=args.host,
      user=args.user,
      password=args.password,
      database=args.database,
      port=port
    ) 
    # print(query)
    cursor  = db_con.cursor()
    cursor.execute(query) 
    db_con.commit() 
    print("Query executed successfully!") 
  except mysql.connector.Error as e: 
    print(f"MySQL error '{e}' occurred") 



# records = get_records(
#   host="localhost",
#   user="user",
#   password="password",
#   database="database",
#   statement="SELECT * FROM table WHERE column1 = 'value'"
# )
