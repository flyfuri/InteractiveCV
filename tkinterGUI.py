##############################################
# this would be the GUI file:

import os
import tkinter as tk
import tkinter.messagebox as tkmsgbox
from functools import partial

class GUI:
    _rootW = None #tk.Tk(screenName="InteractiveCV")
    _frm = None #tk.Frame(_rootW,height=600, width=800)
    _returnvalue = [0,0]
    _colsToSkip = 0

    def __init__(self):
        # Create a Tkinter root window (it won't be displayed)
        self._returnvalue = [0,0]
        self._rootW = tk.Tk(screenName="InteractiveCV")
        #self._frm = tk.Frame(self._rootW,height=600, width=800, )
        self._rootW.geometry("1200x500")
        self._rootW.configure(bg="light blue")
        self._rootW.title("Welcome to my interactive CV")

    def _setWinSize(self, w=0, h=0):
        win_w, win_h = self._rootW.winfo_width() , self._rootW.winfo_height() #ToDo not working allways 1
        winSizestr = str(w if w > 0 else win_w) + "x" + str(h if h > 0 else win_h)
        self._rootW.geometry(winSizestr)

    def _callback_tablebutton(self, x, y):
        self._returnvalue = [x+self._colsToSkip,y]
        self._frm.destroy()
        self._frm.quit()

    def _callback_resfilt(self):
        self._returnvalue = [0,0]
        self._frm.destroy()
        self._frm.quit()

    def _callback_quit(self):
        self._returnvalue = [-1,-1]
        self._rootW.destroy()
   
    def printTable(self, tablerecords, withoutFirstCol=True): 
        self._returnvalue = [-1,-1]
        px, py = 0, 0
        applyMin = lambda x: x if x > 15 else 15
        col_wds = [max([len(str(row[i])) +2 for row in tablerecords]) for i in range(len(tablerecords[1]))]
        col_wds = [(20 if cw < 20 else cw) for cw in col_wds] # apply min cell width 
        
        #winwidth = sum(col_wds)
        #self._setWinSize(w=winwidth)
          
        self._frm = tk.Frame(self._rootW, height=600, width=800, background="light blue", padx=10, pady=10 )
        self._frm.grid()
        self._colsToSkip = 1 if withoutFirstCol else 0
        tk.Label(self._frm, text="To filter, click the corresponding cell.", justify="left", background="light blue").grid(column=1, row=1, columnspan=6, sticky="w")
        tk.Label(self._frm, text="To sort, click the corresponding header cell.", justify="left", background="light blue" ).grid(column=1, row=2, columnspan=6, sticky="w")
        tk.Label(self._frm, text="To change sort order, click header cell off alredy sorted column again.", justify="left", background="light blue" ).grid(column=1, row=3, columnspan=6, sticky="w")
        tk.Label(self._frm, text=" ", justify="left", background="light blue" ).grid(column=1, row=4, columnspan=6)
        xoffs, yoffs = 1, 5
        for y, row in enumerate(tablerecords):
            for x, celltxt in enumerate(row[self._colsToSkip : ]):
                tk.Button(self._frm, text=celltxt, 
                          command=partial(self._callback_tablebutton, x, y), 
                          width=col_wds[x+self._colsToSkip], background=("gray" if y == 0 else "light gray")).grid(column=x+xoffs, row=y+yoffs)
                px, py = x, y
        px = 5
        py += (yoffs+1)
        tk.Button(self._frm, text="reset filter", command=self._callback_resfilt, width=15).grid(column=px, row=py, padx=10, pady=10)
        tk.Button(self._frm, text="quit", command=self._callback_quit, width=15).grid(column=px+1, row=py, padx=10, pady=10)
        self._frm.mainloop()
        return self._returnvalue
  
  
    def showError(self, title, message):
        return tkmsgbox.showerror(title=title, message=message)
  