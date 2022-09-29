import tkinter as tk
from tkinter import ttk

from recovery.config import SYSTEM_FONT, BACKGROUND, WELCOME_MSG

class Welcome(ttk.Frame):
  def __init__(self, parent) -> None:
    ttk.Frame.__init__(self, parent)
    
    tk.Label(self, text="File Recovery Wizard", font=(SYSTEM_FONT, 20, 'bold'), background=BACKGROUND).pack(padx=4, pady=4)

    self.text_frame = tk.Frame(self, background='blue')
    self.info = tk.Text(self.text_frame, font=(SYSTEM_FONT, 14, tk.NORMAL), background=BACKGROUND, wrap='word', height=10)
    self.info.insert("1.0", WELCOME_MSG)
    self.info.configure(state=tk.DISABLED)
    #self.info.pack(expand=True, fill=tk.BOTH)
    tk.Label(self.text_frame, text=WELCOME_MSG, font=(SYSTEM_FONT, 14, tk.NORMAL), background=BACKGROUND, wraplength=325, justify=tk.LEFT).pack()
    self.text_frame.pack(padx=4, pady=8, expand=False)

    self.btn_frame = tk.Frame(self, background='gray85')
    ttk.Button(self.btn_frame, text="Cancel").pack(side=tk.RIGHT, padx=12)
    ttk.Button(self.btn_frame, text="Next").pack(side=tk.RIGHT, padx=4)
    ttk.Button(self.btn_frame, text="Back", state=tk.DISABLED).pack(side=tk.RIGHT, padx=4)
    self.btn_frame.pack(side=tk.BOTTOM, ipady=4, anchor=tk.SE, expand=True, fill=tk.X)