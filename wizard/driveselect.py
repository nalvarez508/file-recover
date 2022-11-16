import tkinter as tk
from tkinter import ttk, messagebox

import sys
import os
import subprocess
import pandas as pd
from io import StringIO

from recovery.config import DRIVE_SELECT_MSG, PADX, SYSTEM_FONT, BACKGROUND, LABEL_SIZE

class DriveSelect(ttk.Frame):
  """Drive selection frame from a list."""
  def __init__(self, parent) -> None:
    ttk.Frame.__init__(self, parent)
    self.frame_title = "Select Physical Drive"
    self.label_text = DRIVE_SELECT_MSG
    self.parent = parent
    self.is_next_enabled = False
    self.physical_drive = None
    self.drives = self._find_drives()
    self.values = [f"{x[1][1]} ({'%.3f'%(x[1][5]/1024/1024/1024)} GB)" for x in list(self.drives.iterrows())]

    self.drive_list = tk.Listbox(self, font=("Helvetica", 12, tk.NORMAL))
    self.drive_list.bind("<<ListboxSelect>>", self._list_callback)
    self.drive_list.pack(padx=PADX, expand=True, fill=tk.BOTH)
    for disk in self.values:
      self.drive_list.insert(tk.END, disk)
  
  def get_selected_disk(self) -> bool:
    """
    Sets the user-selected physical disk.

    Returns
    -------
    bool
        Success or failure.
    """
    def set_in_parent() -> None:
      self.parent.file_select_page.file_report.set_drive(_physical_disk)
      self.is_next_enabled = True
      self.parent.next_status(True)

    _sel = self.drive_list.curselection()
    _physical_disk = self.drives.iloc[_sel]

    # Size mismatch
    if self.parent.file_select_page.file_report.bytes != _physical_disk["Size"]:
      ans = messagebox.askyesno(self.frame_title, f"Selected drive called {_physical_disk['Caption']} ({int(_physical_disk['Size']/1024/1024/1024)} GB) does not match the size of the report drive called {self.parent.file_select_page.file_report.model} ({int(self.parent.file_select_page.file_report.bytes/1024/1024/1024)} GB). Do you want to continue?")
      if ans == True:
        set_in_parent()
        return True
      else:
        return False
    else:
      set_in_parent()
      return True
  
  def _next_(self) -> bool:
    return self.get_selected_disk()
  
  def _list_callback(self, e) -> None:
    self.parent.next_status(True)
    self.is_next_enabled = True

  def _find_drives(self) -> pd.DataFrame:
    """
    Finds all physical drives attached to the system.

    Returns
    -------
    pd.DataFrame
        Found drives.
    """
    # Windows
    if os.name == 'nt':
      _wmic = subprocess.run('wmic diskdrive list brief /format: csv', shell=True, capture_output=True)
      _wmic_decode = _wmic.stdout.decode('ascii')
      drive_info = pd.read_csv(StringIO(_wmic_decode))
      return drive_info
    elif sys.platform == 'darwin':
      _diskutil = subprocess.run("diskutil list | grep /dev | grep -Eo '^[^ ]+'", shell=True, capture_output=True)
      _diskutil_friendly = subprocess.run("diskutil list | grep /dev", shell=True, capture_output=True)
      _diskutil_decode = _diskutil.stdout.decode('ascii')
      _diskutil_friendly_decode = _diskutil_friendly.stdout.decode('ascii')
      disks = _diskutil_decode.split('\n')[:-1]
      disks_friendly = _diskutil_friendly_decode.split(':\n')[:-1]
      csv = 'Node;Caption;DeviceID;Model;Partitions;Size\n'
      for index, disk in enumerate(disks):
        _size = subprocess.run("diskutil info /dev/disk0 | grep 'Disk Size' | grep -Eo '\\([0-9]+[^)]*' | grep -Eo '[0-9]+'", shell=True, capture_output=True)
        _size_decode = _size.stdout.decode('ascii')
        csv += (f";{disks_friendly[index]};{disk};{disk};;{_size_decode}\n")
      drive_info = pd.read_csv(StringIO(csv), sep=';')
      return drive_info
    # Need linux portion... maybe