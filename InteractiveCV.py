##############################################
# this is the main file

import copy
import DB_sqlite
import tkinterGUI

tableName = "Workhistory"

paramDictdefault = {
      "tablename": tableName,
      "cols": "*",
      "wherecond": "", 
      "wherecolumns": "", 
      "whereval": "",
      "searchstrings": "",
      "sortcol": "",
      "ascdesc": "ASC",
}

paramDictWork = copy.deepcopy(paramDictdefault)

# Create a connection to the in-memory database 
conn = DB_sqlite.sqlite3.connect(':memory:')

# Create DB instance with connection
db = DB_sqlite.DatabaseObject(conn)

tblprinter = tkinterGUI.GUI()

#print("initializing simulated database..\n")
#tblprinter.print_help(small=False)

# Insert data into the table
try:
  db.insert_data_into_list(tableName, DB_sqlite.dtlist_period)
  exitApp = False
  answer = [0, 0]
  #read and display original table
  records = db.readDB_Select_parmAsDict(paramDictWork)
  #records = db.readDB_Select(tableName)
  while exitApp == False:
    if answer == [0, 0]:
      #read and display original table
      paramDictWork = copy.deepcopy(paramDictdefault)
      records = db.readDB_Select_parmAsDict(paramDictWork)
      answer = tblprinter.printTable(records)
    elif answer == [-1,-1]:
      exitApp = True
    else:  
      wherecol = str(records[0][answer[0]])
      whereval = str(records[answer[1]][answer[0]])
      if whereval.find(",") > -1: #if several items in column, ask which one
        options = [a.strip() for a in whereval.split(",")]
        options.insert(0,"choose one of those:")
        optrows = [' ' for option in options]
        opttable =[tuple(optrows), tuple(options)]
        #ask filteroptions:
        answer = tblprinter.printTable(opttable, withoutFirstCol=False)
        search_string = options[answer[0]]
        paramDictWork["wherecond"]=f"{wherecol} LIKE ('%{search_string}%')"
        records = db.readDB_Select_parmAsDict(paramDictWork)       
      else:
        paramDictWork["wherecond"]=f"{wherecol} = \'{whereval}\'"
        records = db.readDB_Select_parmAsDict(paramDictWork)      
      if records != None:
        answer = tblprinter.printTable(records)
except Exception as e:        
      tblprinter.showError("Error", str(e))
finally:    
  exit()     
    
# normal exit
del db
del tblprinter
#print("\n\nThank you for taking time to watch my interactive CV! Looking forward to hear from you...")
##############################################