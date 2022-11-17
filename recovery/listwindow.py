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
  """Root class to hold the window containing the list of files in the report and recovery options."""
  def __init__(self) -> None:
    """Initializes the class."""
    super().__init__()

    self.title("File Restore")
    self.configure(background=BACKGROUND)
    self.recover = None
    self.drive = None
    self.isReady = False
    self.deep_columns = ["File name", "File size", "Create date", "Modify date", "Access date", "Path name", "Starting sector"]
    self.deeper_columns = ['File type', 'Position on disk', 'Detected file size', 'Metadata']
    self.last_used_path = None
    self.pbar_label_var = tk.StringVar()

    self.buttons_frame = ttk.Frame(self)
    self.list_frame = ttk.Frame(self)

    self.select_drive_button = ttk.Button(self.buttons_frame, text="Select Drive", command=self.select_drive)
    #self.select_drive_button.pack(padx=4, side=tk.LEFT, anchor=tk.W)
    self.recover_button = ttk.Button(self.buttons_frame, text="Recover", command=self.save_file)
    self.recover_button.pack(padx=4, side=tk.LEFT, anchor=tk.W)
    self.recover_all_button = ttk.Button(self.buttons_frame, text="Recover All", command=self.save_all_files)
    self.recover_all_button.pack(padx=4, side=tk.LEFT, anchor=tk.W)

    self.pbar = ttk.Progressbar(self.buttons_frame, mode='determinate', orient='horizontal', maximum=100, length=200)
    self.pbar_label = ttk.Label(self.buttons_frame, textvariable=self.pbar_label_var)

    self.file_tree = ttk.Treeview(self.list_frame, selectmode='browse', show='headings', height=25)
    self.file_tree.pack(expand=True, fill=tk.BOTH)
    # try:
    #   self.populate_treeview()
    # except AttributeError:
    #   pass
    # self._make_headings()

    self.buttons_frame.pack(anchor=tk.W, padx=4, pady=4, fill=tk.X)
    self.list_frame.pack(padx=4, pady=4, expand=True, fill=tk.BOTH)

    self.wm_protocol('WM_DELETE_WINDOW', self.destroy)
    self.after_idle(self._run_wizard)
    self.mainloop()
  
  def _load_pbar(self, filecount: int=1) -> None:
    self.pbar.pack(padx=14, anchor=tk.CENTER, side=tk.LEFT)
    self.pbar['value'] = 0
    self.pbar['maximum'] = filecount
    self.pbar_label.pack(anchor=tk.CENTER, side=tk.LEFT)
    self.pbar_label_var.set(f'0/{filecount} recovered')
    self.update()
  
  def _unload_pbar(self) -> None:
    self.pbar.pack_forget()
    self.pbar_label.pack_forget()
    self.update()

  def _run_wizard(self) -> None:
    """Starts the recovery wizard. If it is exited, the app closes."""
    self.recover = Wizard(self).run()
    print(self.recover)
    self.update()
    if self.recover == None:
      self.destroy()
      exit(0)
    else:
      try:
        self.drive = PhysicalData(self.recover.physical_drive, self.recover.sector_size)
        self._make_headings()
        self.populate_treeview()
      except PermissionError:
        messagebox.showerror("Administrator Rights Required", "Could not access the drive, please make sure you are running this application as an administrator.")
        self.destroy()
        exit(1)

  def _buttons_check(self, e=None, ready: bool=True):
    if ready:
      for widget in [self.recover_button, self.recover_all_button]:
        widget.configure(state=tk.NORMAL)
    else:
      for widget in [self.recover_button, self.recover_all_button]:
        widget.configure(state=tk.DISABLED)
    self.update_idletasks()

  def save_file(self) -> None:
    _item = self.file_tree.selection()[0]
    if _item != "":
      _this = self.file_tree.item(_item, 'value')
      _default = (self.last_used_path if self.last_used_path != None else os.path.join(os.path.expanduser("~"), _this[0]))
      path = filesavebox(title="Recover File", default=_default)
      if path != None:
        self.last_used_path = os.path.dirname(path)
        self._load_pbar()
        pos_size = (2 if self.recover.deeper else 1)
        pos_sector = (1 if self.recover.deeper else 6)

        _data = self.drive.search(int(_this[pos_sector]), int(_this[pos_size]), self.recover.deeper)
        if not self.drive.save(path, _data):
          messagebox.showerror('Recover File', 'Could not save this file.')

        self.pbar['value'] = 1
        self.pbar_label_var.set('1/1 recovered')
        self._unload_pbar()
  
  def save_all_files(self) -> None:
    """Saves all recovered files to a directory."""
    _default = (self.last_used_path if self.last_used_path != None else os.path.expanduser('~'))
    path = diropenbox(title="Recover All Files", default=_default)
    if path != None:
      self.last_used_path = os.path.dirname(path)
      self._load_pbar(len(self.recover.files))
      x = len(self.recover.files)
      affected_files = []

      for index, row in enumerate(self.recover.files.iterrows()):
        try:
          _base_path = os.path.join(path, os.path.basename(os.path.dirname(row[1]['Path name'])))
          if not os.path.isdir(_base_path):
            os.makedirs(_base_path)
        except OSError:
          _base_path = path
        pos_size = (2 if self.recover.deeper else 1)
        pos_sector = (1 if self.recover.deeper else 6)

        _data = self.drive.search(row[1][pos_sector], row[1][pos_size], self.recover.deeper)
        _path = os.path.join(_base_path, row[1][0])
        if not self.drive.save(_path, _data):
          affected_files.append(f'{row[1][0]}')
        self.pbar['value'] = (index+1)
        self.pbar_label_var.set(f'{index}/{x} recovered')
        self.update()
      
      self._unload_pbar()
      if affected_files != []:
        bad_file_str = ''
        for item in affected_files:
          bad_file_str += f'{item}\n'
        messagebox.showwarning('Recover All Files', f'Could not save these files:\n\n{bad_file_str}')

  def select_drive(self) -> None:
    self.isReady = False
    drive_path = DriveSelectionWindow(self).show()
    print(drive_path)
    if drive_path != None:
      try:
        self.drive = PhysicalData(drive_path, self.recover.sector_size)
        self.isReady = True
        self._buttons_check()
      except PermissionError as e:
        messagebox.showerror("Disk Read Error", f"This program must be running with administrative rights to read physical disks.\n\n{e}")

  def populate_treeview(self) -> None:
    """Populates the list of files."""
    for row in self.recover.files.iterrows():
      self.file_tree.insert('', tk.END, text=row, values=list(row[1]))
    self.update()
    self._buttons_check()

  def _make_headings(self) -> None:
    cols = (self.deeper_columns if self.recover.deeper else self.deep_columns)
    self.file_tree.configure(columns=cols, displaycolumns=cols)
    for col in cols:
      self.file_tree.heading(col, text=col, anchor='w')
      self.file_tree.column(col, minwidth=10, stretch=True, anchor='w')
    self.file_tree["displaycolumns"] = cols

if __name__ == "__main__":
  ListWindow()