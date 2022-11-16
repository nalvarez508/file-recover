import tkinter as tk
from tkinter import ttk, messagebox
from easygui import fileopenbox

import os

from diskutils.recoveredfiles import RecoveredFiles
from recovery.config import FILE_SELECT_MSG, SYSTEM_FONT, BACKGROUND, LABEL_SIZE

class FileSelect(ttk.Frame):
  """Report selection frame with file-open button."""
  def __init__(self, parent) -> None:
    ttk.Frame.__init__(self, parent)
    self.parent = parent
    self.is_next_enabled = True
    self.frame_title = "Open Report"
    self.label_text = FILE_SELECT_MSG
    self.file_name = tk.StringVar(self, value="Nothing selected")
    self.file_report = None

    self.select_file_frame = ttk.Frame(self)
    tk.Label(self.select_file_frame, textvariable=self.file_name, font=(SYSTEM_FONT, 14, 'italic'), background=BACKGROUND).pack(padx=4)
    ttk.Button(self.select_file_frame, text="Select", command=self._prompt_for_file).pack(padx=4)
    self.select_file_frame.pack(padx=4, pady=12)

  def _prompt_for_file(self) -> None:
    """Opens a file dialog."""
    path = fileopenbox(title="Select Report File", default=os.path.expanduser("~"), filetypes=["*.csv"])
    if path != None:
      if path.endswith(".csv"):
        self.file_report = RecoveredFiles(path)
        self.parent.next_status(True)
        self.file_name.set(os.path.basename(path))
        self.is_next_enabled = True
        self.update_idletasks()
      else:
        messagebox.showerror(self.frame_title, f"Unsupported filetype: {path.split('.')[-1]}\nFiles must be of type '.csv'")