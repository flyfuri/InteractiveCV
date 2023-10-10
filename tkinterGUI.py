##############################################
# this would be the GUI file:

import os
import tkinter as tk

class GUI:
    _rootW = None #tk.Tk(screenName="InteractiveCV")
    _frm = None #tk.Frame(_rootW,height=600, width=800)
    _returnvalue = [0,0]

    def __init__(self):
        # Create a Tkinter root window (it won't be displayed)
        self._returnvalue = [0,0]
        self._rootW = tk.Tk(screenName="InteractiveCV")
        self._frm = tk.Frame(self._rootW,height=600, width=800, )
        self._rootW.geometry("1200x800")

    def _setWinSize(self, w=0, h=0):
        win_w, win_h = self._rootW.winfo_width() , self._rootW.winfo_height() #ToDo not working allways 1
        winSizestr = str(w if w > 0 else win_w) + "x" + str(h if h > 0 else win_h)
        self._rootW.geometry(winSizestr)

    def _callback_tablebutton(self,x,y):
        if y > 1:
            self. _returnvalue = [x,y]
            self._frm.destroy

    def _callback_resfilt(self):
        pass
   
    def printTable(self, tablerecords): 
        self._returnvalue = [0,0]

        col_wds = [max([len(str(row[i])) +2 for row in tablerecords]) for i in range(len(tablerecords[1]))]
        #winwidth = sum(col_wds)
        #self._setWinSize(w=winwidth)
        
        self._frm.grid()
        for y, row in enumerate(tablerecords):
            for x, celltxt in enumerate(row):
                tk.Button(self._frm, text=celltxt, command=self._callback_tablebutton(x+1,y+1), width=col_wds[x]).grid(column=x+1, row=y+1)
                px, py = x, y
        tk.Button(self._frm, text="reset filter", command=self._callback_resfilt, width=15).grid(column=px, row=py+4, )
        tk.Button(self._frm, text="quit", command=self._frm.destroy, width=15).grid(column=px+1, row=py+4, padx=10, pady=10)
        self._frm.mainloop()
        return self._returnvalue
  
  
    def showMessage(self, message):
        return self._RootW.messagebox(message)
  