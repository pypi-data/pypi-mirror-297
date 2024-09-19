import tkinter as tk
from . import Main

class HelpWindow(tk.Toplevel):

    def __init__(self,top,item='top'):
        super().__init__(top)
        self.title('Help')
        Main.offset(top,self)
        label = tk.Label(self,text=Help(item),anchor='w',justify='left')
        label.bind('<Configure>', lambda e: label.config(wraplength=label.winfo_width()))
        label.pack(expand=True,fill=tk.BOTH)

def Help(item):
    if item=="top":
        out = "Choose one of the following options:\n" + \
        " 1. Open: Load SIMS data. There are two options:\n" + \
        "   - Cameca: select a folder with .asc files\n" + \
        "   - SHRIMP: select an .op or .pd file (TODO)\n" + \
        " 2. Method: TODO\n" + \
        " 3. Standards: TODO\n" + \
        " 4. Process: TODO\n" + \
        " 5. Export: TODO\n" + \
        " 6. Plot: Plot the time resolved SIMS data\n" + \
        " 7. List: TODO\n" + \
        " 8. Log: View, save or run the session log of openSIMS commands\n" + \
        " 9. Template: TODO\n" + \
        "10. Settings: TODO\n"
    else:
        pass
    return out
