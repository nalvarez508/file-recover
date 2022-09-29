from pprint import isreadable
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from easygui import filesavebox, fileopenbox, diropenbox

import subprocess
import pandas as pd
from io import StringIO
import os
from physicaldata import PhysicalData

from recoveredfiles import RecoveredFiles
from drivepopup import DriveSelectionWindow

class ListWindow(tk.Tk):
  def __init__(self):
    super().__init__()

    self.title("File Restore")
    try:
      self.recover = RecoveredFiles(r"C:\Users\Nick Alvarez\OneDrive - nevada.unr.edu\2022 Fall\CS704 - Digital Forensics\Project\disk report.csv")
    except TypeError:
      exit(1)
    self.drive = None
    self.isReady = False

    self.buttons_frame = ttk.Frame(self)
    self.list_frame = ttk.Frame(self)

    self.select_drive_button = ttk.Button(self.buttons_frame, text="Select Drive", command=self.select_drive)
    self.select_drive_button.pack(padx=4, side=tk.LEFT, anchor=tk.CENTER)
    self.recover_button = ttk.Button(self.buttons_frame, text="Recover", command=self.save_file)
    self.recover_button.pack(padx=4, side=tk.LEFT, anchor=tk.CENTER)
    self.recover_all_button = ttk.Button(self.buttons_frame, text="Recover All")
    self.recover_all_button.pack(padx=4, side=tk.LEFT, anchor=tk.CENTER)

    self.file_tree = ttk.Treeview(self.list_frame, columns=list(self.recover.files.columns), selectmode='browse', show='headings', displaycolumns=list(self.recover.files.columns), height=25)
    self.file_tree.pack(expand=True, fill=tk.BOTH)
    self.populate_treeview()
    self._make_headings()

    self.buttons_frame.pack(padx=4, pady=4)
    self.list_frame.pack(padx=4, pady=4, expand=True, fill=tk.BOTH)

    self.wm_protocol('WM_DELETE_WINDOW', self.destroy)
    self.mainloop()
  
  def _buttonsCheck(self):
    if self.isReady:
      for widget in [self.recover_button, self.recover_all_button]:
        widget.configure(state=tk.NORMAL)
    else:
      for widget in [self.recover_button, self.recover_all_button]:
        widget.configure(state=tk.DISABLED)
    self.update_idletasks()

  def save_file(self):
    _item = self.file_tree.selection()[0]
    if _item != "":
      _this = self.file_tree.item(_item, 'value')
      _default = os.path.join(os.path.expanduser("~"), _this[0])
      path = filesavebox(title="Save Recovered File", default=_default)
      if path != None:
        _data = self.drive.search(int(_this[6]), int(_this[1]))
        self.drive.save(path, _data)

  def select_drive(self):
    self.isReady = False
    _wmic = subprocess.run('wmic diskdrive list brief /format: csv', shell=True, capture_output=True)
    _wmic_decode = _wmic.stdout.decode('ascii')
    drive_info = pd.read_csv(StringIO(_wmic_decode))
    drive_path = DriveSelectionWindow(self, drive_info).show()
    print(drive_path)
    try:
      self.drive = PhysicalData(drive_path, self.recover.sector_size)
    except PermissionError as e:
      messagebox.showerror("Disk Read Error", f"This program must be running with administrative rights to read physical disks.\n{e}")
    self.isReady = True
    self._buttonsCheck()

  def populate_treeview(self):
    for row in self.recover.files.iterrows():
      self.file_tree.insert('', tk.END, text=row, values=list(row[1]))
    self.update()
    self._buttonsCheck()

  def _make_headings(self):
    cols = list(self.recover.files.columns)
    for col in cols:
      self.file_tree.heading(col, text=col, anchor='w')
      self.file_tree.column(col, minwidth=10, stretch=True, anchor='w')
    self.file_tree["displaycolumns"] = cols

if __name__ == "__main__":
  ListWindow()