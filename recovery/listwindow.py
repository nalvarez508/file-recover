from pprint import isreadable
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from easygui import filesavebox, fileopenbox, diropenbox

import os

from wizard.window import Wizard
from diskutils.physicaldata import PhysicalData
from diskutils.recoveredfiles import RecoveredFiles
from drivepopup import DriveSelectionWindow
from recovery.config import BACKGROUND

class ListWindow(tk.Tk):
  def __init__(self) -> None:
    super().__init__()

    self.title("File Restore")
    self.configure(background=BACKGROUND)
    self.recover = None
    self.drive = None
    self.isReady = False
    self.columns = ["File name", "File size", "Create date", "Modify date", "Access date", "Path name", "Starting sector"]

    self.buttons_frame = ttk.Frame(self)
    self.list_frame = ttk.Frame(self)

    self.select_drive_button = ttk.Button(self.buttons_frame, text="Select Drive", command=self.select_drive)
    #self.select_drive_button.pack(padx=4, side=tk.LEFT, anchor=tk.W)
    self.recover_button = ttk.Button(self.buttons_frame, text="Recover", command=self.save_file)
    self.recover_button.pack(padx=4, side=tk.LEFT, anchor=tk.W)
    self.recover_all_button = ttk.Button(self.buttons_frame, text="Recover All")
    self.recover_all_button.pack(padx=4, side=tk.LEFT, anchor=tk.W)

    self.file_tree = ttk.Treeview(self.list_frame, columns=self.columns, selectmode='browse', show='headings', displaycolumns=self.columns, height=25)
    self.file_tree.pack(expand=True, fill=tk.BOTH)
    try:
      self.populate_treeview()
    except AttributeError:
      pass
    self._make_headings()

    self.buttons_frame.pack(anchor=tk.W, padx=4, pady=4)
    self.list_frame.pack(padx=4, pady=4, expand=True, fill=tk.BOTH)

    self.wm_protocol('WM_DELETE_WINDOW', self.destroy)
    self.after_idle(self._run_wizard)
    self.mainloop()
  
  def _run_wizard(self):
    self.recover = Wizard(self).run()
    print(self.recover)
    self.update()
    if self.recover == None:
      self.destroy()
      exit(0)
    else:
      self.populate_treeview()

  def _buttons_check(self, e=None, ready=True):
    if ready:
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
    drive_path = DriveSelectionWindow(self).show()
    print(drive_path)
    if drive_path != None:
      try:
        self.drive = PhysicalData(drive_path, self.recover.sector_size)
        self.isReady = True
        self._buttonsCheck()
      except PermissionError as e:
        messagebox.showerror("Disk Read Error", f"This program must be running with administrative rights to read physical disks.\n\n{e}")

  def populate_treeview(self):
    for row in self.recover.files.iterrows():
      self.file_tree.insert('', tk.END, text=row, values=list(row[1]))
    self.update()
    self._buttonsCheck()

  def _make_headings(self):
    cols = self.columns
    for col in cols:
      self.file_tree.heading(col, text=col, anchor='w')
      self.file_tree.column(col, minwidth=10, stretch=True, anchor='w')
    self.file_tree["displaycolumns"] = cols

if __name__ == "__main__":
  ListWindow()