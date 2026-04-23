from tkinter import PhotoImage
from PIL import Image, ImageTk

APP_ICONS: tuple[PhotoImage]= tuple()

def load_app_icons(theme="default"):
  
  global APP_ICONS

  try:
    s= Image.open(f"./runtime/res/theme_{theme}/icons.png")
    l= []
    for idx in range(0, 64):
      x= (idx % 8) * 16
      y= (idx // 8) * 16
      i= s.crop((x, y, x+16, y+16))
      pi= ImageTk.PhotoImage(i)
      l.append(pi)

    APP_ICONS= tuple(l)

  except Exception as e:
    if theme != "default":
      print(f"Couldn't load theme icons: {theme}, fallback to default ones")
      load_app_icons()
    else:
      print(e)