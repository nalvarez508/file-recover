import tkinter as tk
from tkinter import ttk, messagebox
from click import command
from easygui import fileopenbox

import pandas as pd
from diskutils.recoveredfiles import RecoveredFiles

from wizard.welcome import Welcome
from wizard.fileselect import FileSelect
from wizard.driveselect import DriveSelect
from recovery.config import BACKGROUND, PADX, SYSTEM_FONT, LABEL_SIZE

class Wizard(tk.Toplevel):
  def __init__(self, parent) -> None:
    tk.Toplevel.__init__(self, parent)
    self.title("File Recovery Wizard")
    self.configure(background=BACKGROUND)
    self.minsize(375,375)
    self.geometry("375x375")
    self.maxsize(375, 375)
    self.title_text = tk.StringVar(self, value="File Recovery Wizard")
    self.label_text = tk.StringVar(self)
    self.current_page = 0

    self.title_frame = tk.Frame(self, background='gray85')
    tk.Label(self.title_frame, textvariable=self.title_text, font=(SYSTEM_FONT, 20, 'bold'), background='gray85').pack(padx=4, pady=4)
    self.title_frame.pack(fill=tk.X)

    tk.Label(self, textvariable=self.label_text, font=(SYSTEM_FONT, LABEL_SIZE, tk.NORMAL), background=BACKGROUND, wraplength=350, justify=tk.LEFT).pack(ipadx=PADX, pady=8, expand=False, anchor=tk.W)

    self.welcome_page = Welcome(self)
    self.file_select_page = FileSelect(self)
    self.drive_select_page = DriveSelect(self)
    self.pages = [self.welcome_page, self.file_select_page, self.drive_select_page]

    self.btn_frame = tk.Frame(self, background='gray85')
    self.back_btn = ttk.Button(self.btn_frame, text="Back", state=tk.DISABLED, command=lambda: self.traverse(-1))
    self.next_btn = ttk.Button(self.btn_frame, text="Next", command=lambda: self.traverse(1))
    self.cancel_btn = ttk.Button(self.btn_frame, text="Cancel", command=self.destroy)

    self.cancel_btn.pack(side=tk.RIGHT, padx=12)
    self.next_btn.pack(side=tk.RIGHT, padx=4)
    self.back_btn.pack(side=tk.RIGHT, padx=4)
    self.btn_frame.pack(side=tk.BOTTOM, ipady=4, anchor=tk.SE, expand=True, fill=tk.X)

    self.traverse(0)
    # if self._check_admin() == False:
    #   messagebox.showerror(self.title_text.get(), "This program must be running with administrative rights to read physical disks.")
    #   self.destroy()
    #   exit()

    self.wm_protocol('WM_DELETE_WINDOW', self.destroy)
    #self.mainloop()

  def run(self) -> RecoveredFiles:
    self.wait_window()
    try:
      if not self.file_select_page.file_report.drive.empty:
        return self.file_select_page.file_report
      else: return None
    except AttributeError:
      return None
  
  def next_status(self, status: bool=True) -> None:
    self.next_btn.configure(state=(tk.NORMAL if status else tk.DISABLED))
    self.update_idletasks()
  
  def traverse(self, amt: int) -> None:
    try:
      is_good_to_traverse = self.pages[self.current_page]._next_()
    except AttributeError:
      is_good_to_traverse = True
    
    if is_good_to_traverse:
      if self.current_page+amt == 0:
        self.back_btn.configure(state=tk.DISABLED)
      else: self.back_btn.configure(state=tk.NORMAL)
      if self.current_page+amt >= len(self.pages):
        self.destroy()
      elif self.current_page+amt >= 0:
        if is_good_to_traverse:
          self.pages[self.current_page].pack_forget()
          self.current_page += amt
          self.pages[self.current_page].pack(expand=True, fill=tk.BOTH)

          self.next_status(self.pages[self.current_page].is_next_enabled)
          self.title_text.set(self.pages[self.current_page].frame_title)
          self.label_text.set(self.pages[self.current_page].label_text)
      
        self.update()

  def _check_admin(self) -> bool:
    import os
    import ctypes

    try:
      return (True if os.getuid() == 0 else False)
    except AttributeError:
      return (True if ctypes.windll.shell32.IsUserAnAdmin() != 0 else False)
    return False

if __name__ == "__main__":
  Wizard()