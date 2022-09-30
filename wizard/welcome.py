import tkinter as tk
from tkinter import ttk

from recovery.config import SYSTEM_FONT, BACKGROUND, WELCOME_MSG, LABEL_SIZE, WARNING_MSG

class Welcome(ttk.Frame):
  def __init__(self, parent) -> None:
    ttk.Frame.__init__(self, parent)
    self.frame_title = "File Recovery Wizard"
    self.label_text = WELCOME_MSG
    self.is_next_enabled = True

    tk.Label(self, text=WARNING_MSG, font=(SYSTEM_FONT, LABEL_SIZE, tk.NORMAL), background=BACKGROUND, foreground='red', wraplength=350, justify=tk.LEFT).pack(padx=10, pady=8, expand=False, anchor=tk.W)

    tk.Label(self, text="Click Next to begin.\n", font=(SYSTEM_FONT, LABEL_SIZE, tk.NORMAL), background=BACKGROUND, wraplength=350, justify=tk.LEFT).pack(padx=10, pady=8, expand=False, anchor=tk.W)