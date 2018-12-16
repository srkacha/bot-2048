#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# GUI module generated by PAGE version 4.19
#  in conjunction with Tcl version 8.6
#    Dec 16, 2018 01:20:40 PM CET  platform: Windows NT

import sys

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True

import app_support

def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = tk.Tk()
    app_support.set_Tk_var()
    top = Toplevel1 (root)
    app_support.init(root, top)
    root.mainloop()

w = None
def create_Toplevel1(root, *args, **kwargs):
    '''Starting point when module is imported by another program.'''
    global w, w_win, rt
    rt = root
    w = tk.Toplevel (root)
    app_support.set_Tk_var()
    top = Toplevel1 (w)
    app_support.init(w, top, *args, **kwargs)
    return (w, top)

def destroy_Toplevel1():
    global w
    w.destroy()
    w = None

class Toplevel1:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85' 
        _ana2color = '#ececec' # Closest X11 color: 'gray92' 
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.',background=_bgcolor)
        self.style.configure('.',foreground=_fgcolor)
        self.style.configure('.',font="TkDefaultFont")
        self.style.map('.',background=
            [('selected', _compcolor), ('active',_ana2color)])

        top.geometry("450x250+650+150")
        top.title("2048 Bot")
        top.configure(background="#fff")

        self.Label1 = tk.Label(top)
        self.Label1.place(relx=0.022, rely=0.04, height=30, width=168)
        self.Label1.configure(background="#fff")
        self.Label1.configure(disabledforeground="#a3a3a3")
        self.Label1.configure(font="Arial")
        self.Label1.configure(foreground="#000000")
        self.Label1.configure(text='''Game dimension:''')

        self.dimensionCombo = ttk.Combobox(top)
        self.dimensionCombo.place(relx=0.422, rely=0.04, relheight=0.124
                , relwidth=0.516)
        self.value_list = ['4x4','5x5','8x8']
        self.dimensionCombo.configure(values=self.value_list)
        self.dimensionCombo.configure(textvariable=app_support.combobox)
        self.dimensionCombo.configure(takefocus="")

        self.Label2 = tk.Label(top)
        self.Label2.place(relx=0.022, rely=0.24, height=30, width=97)
        self.Label2.configure(background="#fff")
        self.Label2.configure(disabledforeground="#a3a3a3")
        self.Label2.configure(font="Arial")
        self.Label2.configure(foreground="#000000")
        self.Label2.configure(text='''Algorithm:''')

        self.algCombo = ttk.Combobox(top)
        self.algCombo.place(relx=0.422, rely=0.24, relheight=0.124
                , relwidth=0.516)
        self.value_list = ['Random','Greedy','Monotonic Decreasing','Expectimax']
        self.algCombo.configure(values=self.value_list)
        self.algCombo.configure(textvariable=app_support.combobox)
        self.algCombo.configure(takefocus="")

        self.startButton = tk.Button(top)
        self.startButton.place(relx=0.6, rely=0.76, height=40, width=150)
        self.startButton.configure(activebackground="#ececec")
        self.startButton.configure(activeforeground="#000000")
        self.startButton.configure(background="#005b96")
        self.startButton.configure(disabledforeground="#a3a3a3")
        self.startButton.configure(font="Arial")
        self.startButton.configure(foreground="#fff")
        self.startButton.configure(highlightbackground="#005b96")
        self.startButton.configure(highlightcolor="black")
        self.startButton.configure(pady="0")
        self.startButton.configure(text='''Start''')

if __name__ == '__main__':
    vp_start_gui()





