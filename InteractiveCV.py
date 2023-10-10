##############################################
# this is the main file

import DB_sqlite
import tkinterGUI

alphabet = tuple(map(chr, range(97, 123)))

# Create a connection to the in-memory database 
conn = DB_sqlite.sqlite3.connect(':memory:')

# Create DB instance with connection
db = DB_sqlite.DatabaseObject(conn)

tblprinter = tkinterGUI.GUI()

#print("initializing simulated database..\n")
#tblprinter.print_help(small=False)

# Insert data into the table
db.insert_data_into_list("Periods", DB_sqlite.dtlist_period)

exitApp = False
while exitApp == False:
  #read and display original table
  allrecords = db.readDB_Select("Periods")
  
  answer = tblprinter.printTable(allrecords)
  if answer == [0,0]:
    exitApp = True
  else:
    whereval = allrecords[answer[0]][answer[1]]
    if whereval.find(",") > -1: #if several items in column, ask which one
      options = [a.strip() for a in whereval.split(",")]
      #inpt = 
      #if int(inpt) in range(1,len(options)+1):
        #search_string = options[int(inpt) - 1]  
        #     
      search_string = whereval.split(",")[0].strip()
      wherecol = str(allrecords[0][answer[1]])
      records = db.readDB_Select("Periods", wherecond=f"{wherecol} LIKE ('%{search_string}%')") # replacement not working yet: LIKE ('%' || ? || '%')      
    else:
      records = db.readDB_Select("Periods", wherecond=f"{wherecol} = \'{whereval}\'")      
    if records != None:
      tblprinter.printTable(records)
          
      #tblprinter.showMessage("something went wrong... press enter")
         
          
       
  
    
# normal exit
del db
del tblprinter
#print("\n\nThank you for taking time to watch my interactive CV! Looking forward to hear from you...")
##############################################