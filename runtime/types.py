from tkinter.font import *

class FontCollection(object):
  default: Font= None
  bold: Font= None
  italic: Font= None
  bold_italic: Font= None

  def __init__(self, default):
    self.default= default

    bold= default.copy()
    bold.configure(weight=BOLD)
    self.bold= bold

    italic= default.copy()
    italic.configure(slant=ITALIC)
    self.italic= italic

    bold_italic= default.copy()
    bold_italic.configure(weight=BOLD, slant=ITALIC)
    self.bold_italic= bold_italic