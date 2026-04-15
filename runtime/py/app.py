from tkinter import *
from tkinter import ttk, filedialog, font
from tkinter.font import Font

from datetime import date as Date

from runtime.py.routine import *
from runtime.py import osutils

WINDOW_MIN_WIDTH= 240
WINDOW_MIN_HEIGHT= 100

CONFIG_MAX_RECENTS= 8

class MainApp(object):

  root: Tk
  menu: tuple[Menu]
  font: Font
  recents: list[str]
  
  frame: Frame

  routines: list[Routine]

  def __init__(self):

    osutils.init()

    r= Tk()
    r.title("Fit Tracker")

    ico16 = PhotoImage(file="./runtime/icon/icon16.png")
    r.iconphoto(True, ico16)

    ttk.Style().theme_use("alt")

    r.geometry(F"{WINDOW_MIN_WIDTH}x{WINDOW_MIN_HEIGHT}")
    r.resizable(False, False)
    
    self.font= font.nametofont("TkDefaultFont")

    m= Menu(r)
    m.add_command(label="Open", underline=0, command=self.menu_open, accelerator="O")
    
    mr= Menu(m, tearoff=False)
    m.add_cascade(menu=mr, label="Recent")
    
    r.config(menu=m)

    r.bind("<o>", self.menu_accelerator_open)
    r.bind("<plus>", self.menu_accelerator_increment_sets)
    r.protocol("WM_DELETE_WINDOW", self.win_onclose)

    self.root= r
    self.menu= (m, mr)
    self.recents= []
    
    self.frame= None

    # TODO: make a list, append loaded here
    self.routines= [None,]

    self.file_open_recents()

    self.ui_clear()
    ttk.Label(self.frame, text="No file open").place(relx=.5, rely=.5, y=-15, anchor=CENTER)
    ttk.Label(self.frame, text="Open a file to track...").place(relx=.5, rely=.5, y=5, anchor=CENTER)

    self.file_open_settings()

    if osutils.is_windows():
      r.after(10, lambda: osutils.override_style_windows(r))

    r.mainloop()

  def menu_accelerator_open(self, event):
    self.menu_open()

  def menu_accelerator_increment_sets(self, event):
    if self.data and not self.data.completed:
      self.increment_sets()

  def menu_open(self):
    fn= filedialog.askopenfilename(initialdir="./content", filetypes=(("FitTracker Info File","*.fti"),("Plain Text", "*.txt"),("All files...", "*")))
    if fn:
      self.file_load(fn)

  def menu_recents_clear(self):
    self.recents.clear()
    self.file_save_recents()
    self.menu_refresh_recents()

  def win_onclose(self):
    self.file_save_settings()
    self.root.destroy()

  def win_fixed_size(self, w, h):
    self.root.geometry(f"{w}x{h}")
    self.root.minsize(w, h)

  # ------------------------------------------------------------------------------------ FILE IO
    
  def file_open_settings(self):
    try:

      with open("./runtime/settings.cfg", "rt", encoding="utf-8") as f:

        r= self.root

        ls= f.readline().replace('\n','').replace('\r','').split(";")

        w= max(r.winfo_width(), WINDOW_MIN_WIDTH)
        h= max(r.winfo_height(), WINDOW_MIN_HEIGHT)

        self.root.geometry(f"{w}x{h}+{int(ls[0])}+{ls[1]}")

    except Exception as e:
      print(e)
      print("unable to read settings file")
    
  def file_save_settings(self):
    try:

      with open("./runtime/settings.cfg", "wt", encoding="utf-8") as f:

        r= self.root

        f.write(f"{r.winfo_x()};{r.winfo_y()}")

    except:
      print("unable to write settings file")
    
  def file_open_recents(self):
    try:

      with open("./runtime/recents.ini", "rt", encoding="utf-8") as f:

        ls= f.readlines()
        
        for i,l in enumerate(ls):
          ls[i]= l.replace('\n','').replace('\r','')
        
        self.recents= ls
        self.menu_refresh_recents()

    except:
      print("unable to update recents file")
    
  def file_save_recents(self):
    try:

      with open("./runtime/recents.ini", "wt", encoding="utf-8") as f:

        r= self.recents
        rl= len(r)

        if rl > 0:
          if rl > 1:
            lines= "\n".join(self.recents)
            f.write(lines)
          else:
            f.write(self.recents[0])

    except:
      print("unable to update recents file")

  def file_open(self, filename):
    
    try:
      with open(filename, "rt", encoding="utf-8") as f:

        ld= f.readline().replace('\n','').replace('\r','').split(';')

        name= ld[0]
        completed= False
        days= int(ld[3])
        sets= int(ld[4])

        dr= tuple(int(e) for e in ld[1].split('.'))
        date= Date(dr[2], dr[1], dr[0])
  
        try:
          dl= tuple(int(e) for e in ld[2].split('.'))

          if dl[2] > 0:
            datelast= Date(dl[2], dl[1], dl[0])
            completed = datelast == Date.today() and sets== 0

        except:
          pass

        u= []

        l= f.readline()
        while l:
          ld= l.replace('\n','').replace('\r','').split(';')

          uname= ld[2]
          usets= int(ld[0])
          ureps= int(ld[1])

          u.append(Exercise(uname, usets, ureps))

          l= f.readline()

        data= RoutineData(name, date, completed, days, sets, tuple(u))

        return data

    except Exception as e:
      print("unable to open file")
      print(e)
      return None

  def file_load(self, filename):
    data= self.file_open(filename)
    self.ui_clear()

    # change this to some append

    if data:
      self.add_recents(filename)
      self.routines[0]= Routine(filename, data)
      rframe, redit, rw, rh= self.routines[0].build(self.frame, self.font)
      self.win_fixed_size(rw, rh)
    else: 
      self.routines[0]= None
      ttk.Label(self.frame, width="128px", relief="flat", text="Unable to open file").place(relx=.5, rely=.5, y=-15, anchor=CENTER)

  def add_recents(self, filename):
    if filename in self.recents:
      self.recents.remove(filename)

    self.recents.insert(0, filename)

    if len(self.recents) > CONFIG_MAX_RECENTS:
      self.recents = self.recents[0:CONFIG_MAX_RECENTS-1]

    self.file_save_recents()
    self.menu_refresh_recents()

  # ------------------------------------------------------------------------------------ UI

  def ui_clear(self):

    if self.frame:
      self.frame.destroy()

    f = ttk.Frame(self.root, padding=(4, 4, 4, 4))
    f.pack(fill=BOTH, side=LEFT, expand=True)

    self.frame= f

  def menu_refresh_recents(self):
    m= self.menu[0]
    mr= Menu(self.menu[0], tearoff=False)

    r= self.recents

    if len(r) > 0:
      for e in r:
        mr.add_command(label=e, command= lambda s=e: self.file_load(s))
      mr.add_separator()
      mr.add_command(label="Clear", command=self.menu_recents_clear)

    else:
      mr.add_command(label="No recent files...", state="disabled")

    m.entryconfig("Recent", menu=mr)
    
def __void__():
  pass