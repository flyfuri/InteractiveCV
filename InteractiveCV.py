#############################################
#fill data - would usually go in a separate file

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
   
    
  def readDB_Select(self, table_name, cols="*", wherecond="", tpl_searchstr="", sortcond=""):  
    records = None
    query = "SELECT " + cols + " FROM " + table_name
    if wherecond != "":
      query = query + " WHERE " + wherecond
    if sortcond != "":
      query = query + " ORDER BY " + sortcond
    try:
      if tpl_searchstr=="":
        self.cursor.execute(query)
      else:
        cursor.execute(query, tpl_searchstr)
      records = self.cursor.fetchall()
      if cols == "*":
        query = f"PRAGMA table_info({table_name})" 
        self.cursor.execute(query)
        headers = [i[1] for i in self.cursor.fetchall()]
        records.insert(0,headers)
    except Exception as e:
      print("problem reading from database:" + e)
    else:
      pass #print(" read OK")
    finally:
      return records
      
        
  def __del__(self):
    conn.close()
    print("data base disconnected..")
    
##############################################
# this would be the GUI file:
#another version with a nicer GUI with buttons didn't work in the online implementation of matplotlib:

class GUI:
  def __init__(self):
    self.vline = "|"
    self.hline = "-"
  
  def print_horline(self,colwidths):
    print("+", "-" * (sum(colwidths)-1+len(colwidths)), "+", sep="") #print horizontal line
  
  def print_row(self, values, colwidths):
    line = []
    for i in range(len(colwidths)):
        line.append(str(values[i]).center(colwidths[i]))
    print(self.vline + self.vline.join(line) + self.vline) 
    
    
  def printTable(self, records, col_names="*", withid=False):
    records = [i[1::] for i in records] if withid == False else records #strip id column
    col_wds = [max([len(str(row[i])) +2 for row in records]) for i in range(len(records[1]))]
    self.print_horline(col_wds)
    self.print_row(records[0], col_wds)
    self.print_horline(col_wds)
    for record in records[1::]:
      self.print_row(record, col_wds)
    self.print_horline(col_wds)
    self.print_row(alphabet[:len(col_wds):], col_wds)
    self.print_horline(col_wds)
    
  def print_emptyscreen(self):
    print("\n" * 20)
    
  def print_help(self, small=True):
    if small == False:
      print("<----If needed, please move splitter bar to the left to accommodate table!\n")
      print("Sometimes the online compiler seem to have a timeout, just start again with run")
      
    print("Enter column and row for the cell after which you would like to filter:)")
    print("Example: enter first \"g7\" and then \"2\" to get all entries with python skills")

    
##############################################
# this would be the main file

from time import sleep
  
alphabet = tuple(map(chr, range(97, 123)))

# Create a connection to the in-memory database 
conn = sqlite3.connect(':memory:')

# Create DB instance with connection
db = DatabaseObject(conn)

tblprinter = GUI()

print("initializing simulated database..\n")
tblprinter.print_help(small=False)
sleep(2) #make it look more dramatic ;)

# Insert data into the table
db.insert_data_into_list("Periods", dtlist_period)


while True:
  #read and display original table
  records = db.readDB_Select("Periods")
  
  print("\ncomplete table:")
  tblprinter.printTable(records, withid=True)
  tblprinter.print_help()
  inpt = input("\nEnter column letter and row number or ? for help or ! for exit: ")
  if inpt.lower() == "!":
      break
  elif inpt.lower() == "?":
      tblprinter.print_emptyscreen()
      tblprinter.print_help(small=False)
      tblprinter.print_emptyscreen()
  elif inpt[:1:].lower() in alphabet[:(len(records[0])):] and inpt[1:3:] in [str(i) for i in range(1,len(records))]:
    wherecol = whereval = ""
    for row in records:
      if str(row[0]) == inpt[1:3:]:
        wherecol = str(records[0][alphabet.index(inpt[:1:].lower())])
        whereval = str(row[alphabet.index(inpt[:1:].lower())])
        if whereval.find(",") > -1: #if several items in column, ask which one
          print("\nwhich of the following would you like to filter for:")
          options = [a.strip() for a in whereval.split(",")]
          inpt = input("".join([f"{options[i]}=[{i+1}]  " for i in range(len(options))]))
          if int(inpt) in range(1,len(options)+1):
            search_string = options[int(inpt) - 1]
          else:
            search_string = whereval.split(",")[0].strip()
          records = db.readDB_Select("Periods", wherecond=f"{wherecol} LIKE ('%{search_string}%')") # replacement not working yet: LIKE ('%' || ? || '%')
          tblprinter.print_emptyscreen()
          print(f"{wherecol} \"contains\" {search_string}:")
        else:
          records = db.readDB_Select("Periods", wherecond=f"{wherecol} = \'{whereval}\'")
          tblprinter.print_emptyscreen()
          print(f"{wherecol} = {whereval}:")
          
        if records != None:
          tblprinter.printTable(records, withid=True)
          inpt = input("\npress enter to go back to original table:")
          inpt = ""
          tblprinter.print_emptyscreen()
        else:
          inpt = ("something went wrong... press enter")
          tblprinter.print_emptyscreen()
          
        break #break of for row in records
  else:
    inpt = input("\ninvalid! Do you want to exit: [n]=NO all others =YES ")
    if inpt.lower() != "n":
      break
    
# normal exit
del db
print("\n\nThank you for taking time to watch my interactive CV! Looking forward to hear from you...")
##############################################