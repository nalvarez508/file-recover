import tkinter as tk
from tkinter import ttk, messagebox
from easygui import fileopenbox

import pandas as pd

from wizard.welcome import Welcome
from recovery.config import BACKGROUND

class Wizard(tk.Tk):
  def __init__(self) -> None:
    super().__init__()
    self.title("File Recovery Wizard")
    self.configure(background=BACKGROUND)
    self.minsize(375,375)
    self.geometry("375x375")
    self.maxsize(375, 375)
    self.recovery_data = None

    self.welcome = Welcome(self)
    self.welcome.pack(expand=True, fill=tk.BOTH)

    self.wm_protocol('WM_DELETE_WINDOW', self.destroy)
    self.mainloop()
  
  def run(self) -> pd.DataFrame:
    self.deiconify()
    self.wait_window()
    return self.recovery_data

if __name__ == "__main__":
  Wizard()