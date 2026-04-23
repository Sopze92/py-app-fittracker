from tkinter import *
from tkinter import ttk

class StatusBar(object):

  frame: Frame
  label: StringVar

  def __init__(self):
    self.label= StringVar(value="Hello World")

  def build(self, frame):

    bframe= ttk.Frame(frame, padding=(0,0,0,0))

    s= ttk.Label(bframe, textvariable=self.label)
    s.place(relx=0, rely=0, x=2, y=1, relwidth=1.0, height=20)

    s= ttk.Separator(bframe, orient=HORIZONTAL)
    s.place(relx=0, rely=0, y=1, relwidth=1.0, height=2)

    bframe.pack(fill=X, ipady=10)

    self.frame= bframe

  def set_label(self, label):
    self.label.set(label)

  def clear_label(self):
    self.label.set("")
    
  def height(self): return 20