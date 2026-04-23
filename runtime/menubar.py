from tkinter import *
from tkinter import ttk

from runtime import globals as _G, resources

class MenuBar(object):

  frame: Frame= None
  buttons: tuple[Button]

  menu_recents= Menu

  def build(self, frame):

    app= _G.APP_INSTANCE
    sb= app.statusbar

    if self.frame:
      self.frame.destroy()

    btn= self.__button__
    sep= self.__separator__

    ms= ttk.Style()
    ms.map("MenuBar.TButton", relief="flat")

    bl= []

    bframe= ttk.Frame(frame, padding=(0,0,0,0))

    bl.append(btn(bframe, 2, _G.ICON_NEW, sb, "Create new routine", app.menu_new))
    sep(bframe, 28)
    
    bl.append(btn(bframe, 32, _G.ICON_LOAD, sb, "Load routine file", app.menu_open))
    bl.append(btn(bframe, 54, _G.ICON_RECENTS, sb, "Open recents menu", app.menu_recents))

    sep(bframe, 80)

    bl.append(btn(bframe, 82, _G.ICON_SAVE, sb, "Save current routine", app.menu_save))
    bl.append(btn(bframe, 104, _G.ICON_SAVEAS, sb, "Save current routine as...", app.menu_saveas))
    
    bl[_G.MENUBAR_BUTTON_SAVE].config(state=DISABLED)
    bl[_G.MENUBAR_BUTTON_SAVEAS].config(state=DISABLED)

    s= ttk.Separator(bframe, orient=HORIZONTAL)
    s.place(relx=0, rely=1.0, y=-3, relwidth=1.0, height=2)

    bframe.pack(fill=X, ipady=13)
    
    frame.bind("<Control-n>", app.menu_accelerator_new)
    frame.bind("<Control-o>", app.menu_accelerator_open)
    frame.bind("<Control-s>", app.menu_accelerator_save)
    frame.bind("<Control-Shift-s>", app.menu_accelerator_saveas)

    frame.bind("<plus>", app.menu_accelerator_increment_sets)

    self.frame= bframe
    self.buttons= tuple(bl)

  def __button__(self, frame, x, icon, sb, hovertext, command):
    b= ttk.Button(frame, image=resources.APP_ICONS[icon], padding=(0,0,0,0), command=command, style="MenuBar.TButton")
    b.place(relx=0, rely=0, x=x, width=24, height= 24)
    b.bind("<Enter>", lambda e: self.__showLabel__(sb, b, hovertext))
    b.bind("<Leave>", lambda e: sb.clear_label())
    return b
  
  def __showLabel__(self, statusbar, button, label):
    if not DISABLED in button.state():
      statusbar.set_label(label)
    
  def __separator__(self, frame, x):
    s= ttk.Separator(frame, orient=VERTICAL)
    s.place(relx=0, rely=0, x=x, width=2, height=22)

  def height(self): return 26

  def on_document_ready(self, isfile):
    self.buttons[_G.MENUBAR_BUTTON_SAVE].config(state=NORMAL if isfile else DISABLED)
    self.buttons[_G.MENUBAR_BUTTON_SAVEAS].config(state=NORMAL)