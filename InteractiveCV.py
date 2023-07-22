#############################################
#fill data - would usually go in a separate file

# data
dtlist_period = [("id[INTEGER PRIMARY KEY]", "start[DATE NOT NULL]", "end[DATE  NOT_NULL]", "companyID[Text]", "title[TEXT]", "role[TEXT]", "Lang_ID[TEXT]", ),
          (1, "1995-08-01", "1999-05-31", "Company A", "Electric Mechanic", "Apprentice", "1",),
          (2, "2000-11-01", "2001-11-30", "Company B", "Maintenance Mechanic and Electrician", "PLC_Programmer", "1",)]

company = [("id[INTEGER PRIMARY KEY]", "Departement", ),
            ("Phone", 800),
            ("Headphones", 150)]


import sqlite3

class DatabaseObject:
  def __init__(self, connection):
    self.conn = connection
    self.cursor = self.conn.cursor()

  def insert_data_into_list(self, table_name, data_list):
    col_names = [col.split('[')[0] for col in data_list[0]]
    col_infos = [col.split('[')[1].split(']')[0] for col in data_list[0]]
    print(col_names)
    print(col_infos)
    placeholders = ', '.join(['?'] * len(data_list[0]))
    print(placeholders)
    query_create_table = "CREATE TABLE IF NOT EXISTS " + table_name + " ("
    for i in range(len(col_names)):
      query_create_table = query_create_table + col_names[i] + " " + (col_infos[i] if i < len(col_infos) else "") + ("," if i < len(col_names)-1 else ")")
    print(query_create_table)
    insert_query = f"INSERT INTO {table_name} (" + ",".join(col_names) + f") VALUES ({placeholders})"
    print(insert_query) 
        
    try:       
      self.cursor.execute(query_create_table)
      self.cursor.executemany(insert_query, data_list[1:])  # Assuming the first tuple is for column names and types
            
    except Exception as e:
      print(e)
    else:
      print("OK")
        
        
  def __del__(self):
    conn.close()
    print("thanks for watching")

# Create a connection to the in-memory database
conn = sqlite3.connect(':memory:')

# Create DB instance with connection
db = DatabaseObject(conn)

# Insert data into the table
db.insert_data_into_list("Periods", dtlist_period)



import matplotlib.pyplot as plt
from matplotlib.widgets import Button

table_data = [['Cell 1', 'Cell 2'],
              ['Cell 3', 'Cell 4'],
              ['Cell 5', 'Cell 6']]
              
class PlotExitException(Exception):
    pass

fig, ax = plt.subplots()

# hide axes
fig.patch.set_visible(False)
ax.axis('off')
ax.axis('tight')

ax.table = ax.table(cellText=table_data, loc='center')

#ax.table(cellText=df.values, colLabels=df.columns, loc='center')

fig.tight_layout()

# button 1
axBtn1 = plt.axes([0.4, 0.01, 0.1, 0.1])
btn1 = Button(axBtn1, label="1", color='white', hovercolor='white')
  
def __btn1(event):
  table_data = [['Cell 11', 'Cell 12'],
              ['Cell 13', 'Cell 14']]
  ax.table = ax.table(cellText=table_data, loc='center')          
  fig.canvas.draw()
  
btn1.on_clicked(__btn1)

# button exit
axBtnExit = plt.axes([0.9, 0.01, 0.09, 0.1])
btnExit = Button(axBtnExit, label="X exit", color='white', hovercolor='white')
  
def __closeApp(event):
  plt.close()
  raise PlotExitException
 
btnExit.on_clicked(__closeApp)


try:
  plt.show()
except PlotExitException:
  del db
finally:
  print("end")

while True:
  b  = input("enter:")
  print(b)
  if b == 1:
    table_data = [['Cell 11', 'Cell 12'],['Cell 13', 'Cell 14']]
    ax.table = ax.table(cellText=table_data, loc='center')  
    plt.show()
  else: 
    break
##############################################
