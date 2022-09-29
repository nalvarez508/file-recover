import tkinter as tk
from tkinter import ttk

class DriveSelectionWindow(tk.Toplevel):
  def __init__(self, parent, drives):
    tk.Toplevel.__init__(self, parent)
    self.title("Select Drive")
    self.radios = []
    self.drive_info = drives
    self.selection = tk.IntVar(self, value=0)

    self.radio_frame = ttk.Frame(self)

    for index, drive in enumerate(drives.iterrows()):
      self._makeEntry(list(drive[1]), index)
    
    self.radio_frame.pack(padx=4, pady=2)
    ttk.Button(self, text="Select", command=self.destroy).pack(padx=4, pady=2)
  
  def _makeEntry(self, entry, index):
    ttk.Radiobutton(self.radio_frame, text=f"{entry[1]} ({entry[5]/1024/1024/1024} GB)", value=index, variable=self.selection).pack(padx=4, pady=2, anchor=tk.W)

  def show(self):
    self.deiconify()
    self.wait_window()
    return list(self.drive_info.iterrows())[self.selection.get()][1][2]