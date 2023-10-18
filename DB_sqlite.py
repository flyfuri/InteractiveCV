#############################################
#all database functions

# data
dtlist_period = [("id[INTEGER PRIMARY KEY]", "Begin[DATE NOT NULL]", "End[DATE  NOT_NULL]", "Company[Text]", "Department[TEXT]", "Role[TEXT]", "Skills[TEXT]", ),
          (1, "1995-08-01", "1999-05-31", "Company A", "several", "Apprentice", "mech. manufact, electric",),
          (2, "2000-06-01", "2001-11-30", "Company B", "Maintenance", "Electric Mechanic", "mech. and elec. maintenance",),
          (3, "2001-12-01", "2004-04-30", "Company B", "Industrialization department", "Technician", " PLC, Electrical wiring, drawing el.schematics",),
          (4, "2004-05-01", "2011-11-30", "School", "Advanced Diploma..", "Software Engineer", "C++",),
          (5, "2004-05-01", "2011-11-30", "Company B", "Industrialization department", "Software Engineer", "PLC, LabView",),
          (6, "2011-01-01", "2022-09-30", "Company C", "Developement/Support", "Software Engineer", "PLC, LabView, GIT",),
          (7, "2023-01-01", "2023-06-30", "private study", "projects and certification", "Software Engineer", "C++, Python, embedded(arduino&co), GIT",)]


import sqlite3

class DatabaseObject:
  def __init__(self, connection):
    self.conn = connection
    self.cursor = self.conn.cursor()

  def insert_data_into_list(self, table_name, data_list):
    col_names = [col.split('[')[0] for col in data_list[0]]
    col_infos = [col.split('[')[1].split(']')[0] for col in data_list[0]]
    placeholders = ', '.join(['?'] * len(data_list[0]))
    query_create_table = "CREATE TABLE IF NOT EXISTS " + table_name + " ("
    for i in range(len(col_names)):
      query_create_table = query_create_table + col_names[i] + " " + (col_infos[i] if i < len(col_infos) else "") + ("," if i < len(col_names)-1 else ")")
    insert_query = f"INSERT INTO {table_name} (" + ",".join(col_names) + f") VALUES ({placeholders})"
        
    try:       
      self.cursor.execute(query_create_table)
      self.cursor.executemany(insert_query, data_list[1:])  # Assuming the first tuple is for column names and types
            
    except Exception as e:
      print("problem writing database:" + e)
  
  #def readDB_Select(self, table_name, cols="*", wherecond="", tpl_searchstr="", sortcond=""):
  def readDB_Select(self, table_name, cols="*", wherecond="", sortcond=""):
    records = None
    query = "SELECT " + cols + " FROM " + table_name
    if wherecond != "":
      query = query + " WHERE " + wherecond
    if sortcond != "":
      query = query + " ORDER BY " + sortcond
    try:
      #if tpl_searchstr=="":
      self.cursor.execute(query)
      #else:
      #  cursor.execute(query, tpl_searchstr)
      records = self.cursor.fetchall()
      if cols == "*":
        query = f"PRAGMA table_info({table_name})" 
        self.cursor.execute(query)
        headers = tuple([i[1] for i in self.cursor.fetchall()])
        records.insert(0,headers)
    except Exception as e:
      pass #print("problem reading from database:" + e)
    else:
      pass #print(" read OK")
    finally:
      return records
    
  
        
  def __del__(self):
    self.conn.close()
    print("data base disconnected..")
    