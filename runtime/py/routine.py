from tkinter import *
from tkinter import ttk
from datetime import date as Date

class UI_TableEntry(object):
  sets: Label
  reps: Label
  name: Label

  def __init__(self, sets, reps, name):
    self.sets= sets
    self.reps= reps
    self.name= name

  def set_enabled(self, state):
    color= "black" if state else "#969696"
    labels= (self.sets, self.reps, self.name)
    for l in labels:
      l.config(foreground= color)
  
class UI_Table(object):
  entries: tuple[UI_TableEntry]

  def __init__(self, entries):
    self.entries= entries

class UI_Data(object):
  table: UI_Table
  btn_edit: Button
  btn_increment: Button
  btn_unlock: Button
  label_days: StringVar
  label_reps: StringVar
  label_done: StringVar

  def __init__(self):
    self.label_days= StringVar(value= "days: 0")
    self.label_reps= StringVar(value= "0/0")
    self.label_done= StringVar(value= "")

class Exercise(object):

  name: str
  sets: int
  reps: int

  def __init__(self, name:str, sets:int, reps:int):
    self.name= name
    self.sets= sets
    self.reps= reps

class RoutineData(object):

  name: str
  date: Date
  completed: bool
  days: int
  sets: int
  exercises: tuple[Exercise]
  
  sets_max: int
  unlocked: bool
  edit: bool

  def __init__(self, name:str, date:Date, completed:bool, days:int, sets:int, exercises:tuple[Exercise]):
    self.sets_max= max(e.sets for e in exercises)
    self.unlocked= not completed
    self.edit= False

    self.name= name
    self.date= date
    self.completed= completed
    self.days= days
    self.sets= self.sets_max if completed else sets
    self.exercises= exercises

class Routine(object):
  
  filename: str
  data: RoutineData
  ui: UI_Data

  def __init__(self, filename, data):
    self.filename= filename
    self.data= data
    self.ui= UI_Data()

  def increment_sets(self):
    d= self.data

    d.sets+= 1
    if d.sets >= d.sets_max:
      d.days+= 1
      d.completed= True
      d.unlocked= False

    self.save_file()
    self.ui_refresh()

  def unlock_sets(self):
    d= self.data
    d.completed= False
    d.unlocked= True
    d.sets= 0

    self.ui_refresh()

  def save_file(self):
    try:

      lines= []
      d= self.data

      with open(self.filename, "rt", encoding="utf-8") as f:
        lines= f.readlines()
        l0= lines[0].replace('\r','').replace('\n','').split(";")
        if d.completed:
          t= Date.today()
          l0[2]= f"{t.day}.{t.month}.{t.year}"
        l0[3]= str(d.days)
        l0[4]= "0" if d.completed else str(d.sets)
        lines[0]= ';'.join(l0) + "\n"
    
      with open(self.filename, "wt", encoding="utf-8") as f:
        f.writelines(lines)

    except:
      print("unable to save file")

  def toggle_edit(self):
    d= self.data
    d.edit= not d.edit
    self.build()
   
  def build(self, frame, font) -> tuple[Frame, Button, int, int]:

    d= self.data

    # header
    gframe= ttk.Frame(frame, padding=(2, 2, 2, 2))

    be= ttk.Button(gframe, text="edit")
    be.place(relx=0, rely=0, x=-2, y=0, width=32, height=24, anchor=NW)
    self.ui.btn_edit= be

    if d.edit:
      _e= ttk.Entry(gframe, textvariable=d.name)
      _e.insert(0, d.name)
      _e.place(relx=0.5, rely=0, y=4, anchor = CENTER)
    else:
      l= ttk.Label(gframe, text=d.name)
      l.place(relx=0.5, rely=0, y=4, anchor = CENTER)
      #l.bind("<Double-1>", lambda e:self.edit_element(LABEL_TITLE))

    ttk.Label(gframe, text=d.date).place(relx=0.5, rely=0, y=24, anchor = CENTER)

    # days
    ttk.Label(gframe, textvariable=self.ui.label_days).place(relx=1.0, rely=0, x=0, y=24, anchor=E)

    # table
    tframe= ttk.Frame(gframe)

    # table header
    thframe= ttk.Frame(tframe, relief="groove", padding=(8,2,8,2))
    ttk.Label(thframe, text="sets").place(relx=0, rely=0, x=0, anchor=NW)
    ttk.Label(thframe, text="reps").place(relx=0, rely=0, x=60, anchor=N)
    ttk.Label(thframe, text="name").place(relx=1.0, rely=0, x=0, anchor=NE)
    thframe.place(relx=0, rely=0, relwidth=1.0, height=24)
    
    # table content
    tdframe= ttk.Frame(tframe, relief="flat" if d.edit else "groove", padding=(8,2,8,2))
    h_table= 20*len(d.exercises)
    table_entries= []
    lun= ""

    if d.edit:
      for i,u in enumerate(d.exercises):
        us= ttk.Entry(tdframe, textvariable=u.sets)
        us.place(relx=0, rely=0, x=-4, y=20*i, width= 30, anchor=NW)
        ur= ttk.Entry(tdframe, textvariable=u.reps)
        ur.place(relx=0, rely=0, x=60, y=20*i, width= 30, anchor=N)
        un= ttk.Entry(tdframe, textvariable=u.name)
        un.place(relx=1.0, rely=0, x=4, y=20*i, anchor=NE)
        table_entries.append(UI_TableEntry(us, ur, un))
    else:
      for i,u in enumerate(d.exercises):
        us= ttk.Label(tdframe, text=u.sets)
        us.place(relx=0, rely=0, x=0, y=20*i, anchor=NW)
        ur= ttk.Label(tdframe, text=u.reps)
        ur.place(relx=0, rely=0, x=60, y=20*i, anchor=N)
        un= ttk.Label(tdframe, text=u.name)
        un.place(relx=1.0, rely=0, x=0, y=20*i, anchor=NE)
        table_entries.append(UI_TableEntry(us, ur, un))

    sun= un.cget("text")
    if len(sun) > len(lun):
      lun= sun

    self.ui.table= UI_Table(tuple(table_entries))

    tdframe.place(relx=0, rely=0, y=22, relwidth=1.0, height=h_table+4)
    
    tframe.place(relx=0.5, rely=0, x=0, y=38, relwidth=1.0, height= h_table+28, anchor=N)

    # day done / reps
    ttk.Label(gframe, textvariable=self.ui.label_done).place(relx=1.0, rely=0, x=-64, y=h_table+78, anchor=E)
    ttk.Label(gframe, textvariable=self.ui.label_reps).place(relx=1.0, rely=0, x=-28, y=h_table+78, anchor=E)

    bi= ttk.Button(gframe, text="+", command=self.increment_sets)
    bi.place(relx=1.0, rely=0, x=2, y=h_table+78, width=24, height=24, anchor=E)
    self.ui.btn_increment= bi

    bu= ttk.Button(gframe, text="unlock", command=self.unlock_sets)
    bu.place(relx=0, rely=0, x=-2, y=h_table+78, width=50, height=24, anchor=W)
    self.ui.btn_unlock= bu

    gframe.pack(fill="both", expand=True)

    ww= max(font.measure(lun) + 24 + 90, 240)
    wh= h_table + 100

    self.ui_refresh()

    return (gframe, be, ww, wh)
  
  def ui_refresh(self):

    d= self.data
    lock= d.completed and not d.unlocked
    
    if d.edit:
      self.ui.label_reps.set(f"?/{d.sets_max}")
      self.ui.label_days.set(f"days: ?")

      self.ui.btn_increment.state(['disabled'])
      self.ui.btn_unlock.state(["disabled"])
      self.ui.btn_unlock.place(relx=-1.0, width=0)

      for e in self.ui.table.entries:
        e.set_enabled(True)

    else:

      self.ui.label_reps.set(f"{d.sets}/{d.sets_max}")
      self.ui.label_days.set(f"days: {d.days}")

      if lock:
        self.ui.label_done.set("day completed!")
        self.ui.btn_increment.state(['disabled'])
        self.ui.btn_unlock.state(["!disabled"])
        self.ui.btn_unlock.place(relx=0, width=50)
      else:
        self.ui.label_done.set("")
        self.ui.btn_increment.state(['!disabled'])
        self.ui.btn_unlock.state(["disabled"])
        self.ui.btn_unlock.place(relx=-1.0, width=0)

      for e in self.ui.table.entries:
        e.set_enabled(not lock and d.sets < int(e.sets.cget("text")))