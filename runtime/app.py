from tkinter import *
from tkinter import ttk, filedialog, font

from datetime import date as Date

from runtime import globals as _G, osutils, resources
from runtime.types import FontCollection

from runtime.routine import *
from runtime.menubar import MenuBar
from runtime.statusbar import StatusBar

WINDOW_MIN_WIDTH= 240
WINDOW_MIN_HEIGHT= 100

CONFIG_MAX_RECENTS= 8

class MainApp(object):

  root: Tk
  font_default: FontCollection

  recents: list[str]
  recents_menu: Menu= None

  menubar: MenuBar
  statusbar: StatusBar
  
  content: Frame
  data: Frame

  routines: list[Routine]

  def __init__(self):

    _G.APP_INSTANCE= self

    osutils.init()

    r= Tk()
    r.title("Fit Tracker")

    ico16 = PhotoImage(file="./runtime/icon/icon16.png")
    r.iconphoto(True, ico16)
    
    resources.load_app_icons()

    self.setup_styles()

    r.geometry(F"{WINDOW_MIN_WIDTH}x{WINDOW_MIN_HEIGHT}")
    r.resizable(False, False)
    
    self.font_default= FontCollection(font.nametofont("TkDefaultFont"))

    r.protocol("WM_DELETE_WINDOW", self.win_onclose)

    self.root= r
    self.recents= []

    mb= MenuBar()
    self.menubar= mb

    sb= StatusBar()
    self.statusbar= sb

    mb.build(r)
    self.content= ttk.Frame(r, padding=(0,4,0,4))
    self.content.pack(fill=BOTH, expand=True)
    self.data= None
    sb.build(r)

    self.ui_empty()

    # TODO: make a list, append loaded here
    self.routines= [None,]

    self.read_recents_file()
    self.read_settings_file()

    if osutils.is_windows():
      r.after(10, lambda: osutils.override_style_windows(r))

    r.mainloop()

  def setup_styles(self):
    
    bs= ttk.Style()
    bs.theme_use("alt")

    bs.element_create("Button.Increment.image", "image", 
      resources.APP_ICONS[_G.ICON_INCREMENT],
      ("disabled", resources.APP_ICONS[_G.ICON_INCREMENT_DISABLED]),
      sticky=""
    )

    bs.layout("Routine.Increment.TButton", [
      ("Button.border", { "sticky": NSEW, "children": [
          ("Button.Increment.image", {"sticky": NSEW })
        ]
      })
    ])

    bs.element_create("Button.Edit.image", "image", 
      resources.APP_ICONS[_G.ICON_EDIT],
      ("disabled", resources.APP_ICONS[_G.ICON_EDIT_DISABLED]),
      sticky=""
    )

    bs.layout("Routine.Edit.TButton", [
      ("Button.border", { "sticky": NSEW, "children": [
          ("Button.Edit.image", {"sticky": NSEW })
        ]
      })
    ])

    bs.element_create("Button.Unlock.image", "image", 
      resources.APP_ICONS[_G.ICON_UNLOCK],
      ("disabled", resources.APP_ICONS[_G.ICON_UNLOCK_DISABLED]),
      sticky=""
    )

    bs.layout("Routine.Unlock.TButton", [
      ("Button.border", { "sticky": NSEW, "children": [
          ("Button.Unlock.image", {"sticky": NSEW })
        ]
      })
    ])

  def menu_accelerator_new(self, event): self.menu_new()
  def menu_accelerator_open(self, event): self.menu_open()
  def menu_accelerator_save(self, event): self.menu_save()
  def menu_accelerator_saveas(self, event): self.menu_saveas()

  def menu_accelerator_increment_sets(self, event):
    print("increment_sets")

  def menu_new(self):
    print("new")

  def menu_open(self):
    fn= filedialog.askopenfilename(initialdir="./content", filetypes=(("FitTracker Info File","*.fti"),("Plain Text", "*.txt"),("All files...", "*")))
    if fn:
      self.file_load(fn)

  def menu_recents(self):
    r= self.root
    self.recents_menu.tk_popup(r.winfo_rootx() + 54, r.winfo_rooty() + 24)

  def menu_save(self):
    self.routines[0].save_file()

  def menu_saveas(self):
    fn= filedialog.asksaveasfilename(initialdir="./content", filetypes=(("FitTracker Info File","*.fti"),("Plain Text", "*.txt"),("All files...", "*")))
    if fn:
      self.routines[0].save_file(fn)

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
    
  def read_settings_file(self):
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
    
  def read_recents_file(self):
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
        datestart= Date(dr[2], dr[1], dr[0])
        datelast= None
  
        try:
          dl= tuple(int(e) for e in ld[2].split('.'))

          if dl[2] > 0:
            datelast= Date(dl[2], dl[1], dl[0])
            completed = datelast == Date.today() and sets== 0

        except:
          pass

        date= (datestart, datelast)

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
    self.ui_clear_content()

    # change this to some append

    if data:
      self.add_recents(filename)
      self.routines[0]= Routine(filename, data)
      rframe, redit, rw, rh= self.routines[0].build(self.data)
      bh= self.menubar.height() + self.statusbar.height()
      self.win_fixed_size(rw, rh+bh)
      self.menubar.on_document_ready(True)
    else: 
      self.routines[0]= None
      ttk.Label(self.data, width="128px", relief="flat", text="Unable to open file").place(relx=.5, rely=.5, y=-15, anchor=CENTER)

  def add_recents(self, filename):
    if filename in self.recents:
      self.recents.remove(filename)

    self.recents.insert(0, filename)

    if len(self.recents) > CONFIG_MAX_RECENTS:
      self.recents = self.recents[0:CONFIG_MAX_RECENTS-1]

    self.file_save_recents()
    self.menu_refresh_recents()

  # ------------------------------------------------------------------------------------ UI

  def ui_clear_content(self):

    if self.data:
      self.data.destroy()

    f = ttk.Frame(self.content, padding=(0,0,0,0))
    f.pack(fill=BOTH, side=LEFT, expand=True)

    self.data= f

  def menu_refresh_recents(self):

    if self.recents_menu:
      self.recents_menu.destroy()

    mr= Menu(tearoff=False)

    r= self.recents

    if len(r) > 0:
      for e in r:
        mr.add_command(label=e, command= lambda s=e: self.file_load(s))
      mr.add_separator()
      mr.add_command(label="Clear", command=self.menu_recents_clear)

    else:
      mr.add_command(label="No recent files...", state="disabled")

    self.recents_menu= mr

  def ui_empty(self):
    self.ui_clear_content()

    ttk.Label(self.data, text="No file open").place(relx=.5, rely=.5, y=-10, anchor=CENTER)
    ttk.Label(self.data, text="Open a file to track...").place(relx=.5, rely=.5, y=10, anchor=CENTER)
    
def __void__():
  pass