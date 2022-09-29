import tkinter as tk
from tkinter import ttk

import pandas as pd
import subprocess
from io import StringIO
import sys, os

from recovery.config import BACKGROUND

class DriveSelectionWindow(tk.Toplevel):
  def __init__(self, parent: tk.Tk, radio: bool=False) -> None:
    tk.Toplevel.__init__(self, parent, background=BACKGROUND)
    self.title("Select Drive")
    self.radios = []
    self.drive_info = self.find_drives()
    self.selection = tk.StringVar(self)
    self.user_response = None

    self.radio_frame = ttk.Frame(self)

    if radio:
      for index, drive in enumerate(self.drive_info.iterrows()):
        self._make_entry(list(drive[1]), index)
    else:
      self.values = [f"{x[1][1]} ({'%.3f'%(x[1][5]/1024/1024/1024)} GB)" for x in list(self.drive_info.iterrows())]
      self.cb = ttk.Combobox(self.radio_frame, width=40, textvariable=self.selection, values=self.values)
      self.selection.set(self.values[0])
      self.cb.pack(padx=4,pady=2)

    
    self.radio_frame.pack(padx=4, pady=2)
    ttk.Button(self, text="Select", command=self._validate).pack(padx=4, pady=2)
  
  def find_drives(self) -> pd.DataFrame:
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

  def _make_radio_entry(self, entry: list, index: int) -> None:
    ttk.Radiobutton(self.radio_frame, text=f"{entry[1]} ({'%.3f'%(entry[5]/1024/1024/1024)} GB)", value=index, variable=self.selection).pack(padx=4, pady=2, anchor=tk.W)

  def show(self) -> int:
    self.deiconify()
    self.wait_window()
    return self.user_response
  
  def _validate(self) -> None:
    try:
      self.user_response = list(self.drive_info.iterrows())[int(self.selection.get())][1][2]
    except ValueError:
      self.user_response = list(self.drive_info.iterrows())[self.values.index(self.selection.get())][1][2]
    self.destroy()