import platform
import ctypes as ct 

from tkinter import *

OS_UNKNOWN= 0
OS_WIN= 1
OS_UNIX= 2
OS_MAC= 3

CURRENT_OS= None

def init():
  global CURRENT_OS
  name= platform.system().lower()
  
  if "windows" in name:
    CURRENT_OS= OS_WIN
  elif any("linux", "unix") in name:
    CURRENT_OS= OS_UNIX
  elif any("darwin", "mac", "osx") in name:
    CURRENT_OS= OS_MAC

def is_windows(): return CURRENT_OS == OS_WIN
def is_linux(): return CURRENT_OS == OS_UNIX
def is_mac(): return CURRENT_OS == OS_MAC

def override_style_windows(root):
    set_window_pos = ct.windll.user32.SetWindowPos
    set_window_long = ct.windll.user32.SetWindowLongPtrW
    get_window_long = ct.windll.user32.GetWindowLongPtrW
    get_parent = ct.windll.user32.GetParent

    hwnd = get_parent(root.winfo_id())

    # gwl_style -16 ; ws_minimizebox 131072 | ws_maximizebox 65536
    set_window_long(hwnd, -16, get_window_long(hwnd, -16) & ~196608) 

    # swp_nozorder 4 | swp_nomove 2 | swp_nosize 1 | swp_framechanged 32
    set_window_pos(hwnd, 0, 0, 0, 0, 0, 39)
