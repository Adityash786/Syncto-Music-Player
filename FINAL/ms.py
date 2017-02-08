import os
import pygame
import tkFont,tkFileDialog
from Tkinter import *
import Tkinter
import client

pygame.init()

app = Tk()
app.title('MusicNet 1.0 Beta')

F =Canvas( bd=4, bg="white", height=400,width =500)

peers=client.connect()
def browse():
    file1 = tkFileDialog.askopenfile(parent=app, mode='rb',title='Choose a file')
    name = file1.name
    namee = name.split('/')
    t='play'+' '+namee[len(namee)-1]
    client.control(t,peers)

def track1():
    file1 = "music.mp3"
    file1='play'+' '+file1
    client.control(file1,peers)
def track2():
    file1 = "music0.mp3"
    file1='play'+' '+file1
    client.control(file1,peers)

def volup():
    value=pygame.mixer.music.get_volume()
    value+=0.1
    pygame.mixer.music.set_volume(value)

def voldown():
    value=pygame.mixer.music.get_volume()
    value-=0.1
    pygame.mixer.music.set_volume(value)

def stop():
    client.control('stop',peers)

def pause() :
    client.control('pause',peers)

def unpause() :
    client.control('unpause',peers)

def quit():
    app.quit()

logo = PhotoImage(file="123.gif")
helv36 = tkFont.Font(family='Helvetica', size=36, weight=tkFont.BOLD)
helv24 = tkFont.Font(family='Helvetica', size=24, weight=tkFont.BOLD)
helv18 = tkFont.Font(family='Helvetica', size=18, weight=tkFont.BOLD)
helv15 = tkFont.Font(family='Helvetica', size=15, weight=tkFont.BOLD)
topFrame = Frame(app)
topFrame.pack()
bottomFrame = Frame(app)
bottomFrame.pack(side=BOTTOM)
one = Label(app, text="HACK **1.0**", font=helv36, bg="black", fg="white")
one.pack()

four = Label(app, text=u"\u266b Network Music Player \u266b ", font="Helvetica 24 bold italic", bg="sky blue", fg="maroon")
four.pack(fill=X)
w = Label(app, compound = CENTER,image=logo).pack()

fou = Label(app, bg="navy blue", fg="white")
fou.pack(fill=X)
var = IntVar()

menu = Menu(app)
app.config(menu=menu)

subMenu = Menu(menu)
menu.add_cascade(label="TrackList", menu=subMenu)
subMenu.add_command(label="Let me love you", command=track1)
subMenu.add_command(label="Bulleya", command=track2)

subMenu1 = Menu(menu)
menu.add_cascade(label="Search track", menu=subMenu1)
subMenu1.add_command(label="Browse", command=browse)

'''subMenu2 = Menu(menu)
menu.add_cascade(label="Users", menu=subMenu)
for n in peers
	subMenu2.add_command(label=n) 
'''
ps3 = Label(app, text="                   ", font=helv24)
ps3.pack(side=LEFT)
'''ps = Button(app, text="Play", font=helv15, command=play, bg="pink", fg="maroon")
ps.pack(side=LEFT)'''
ps3 = Label(app, text="        ", font=helv24)
ps3.pack(side=LEFT)
ps10 = Button(app, text="VOL+", font=helv15, command=volup, bg="pink", fg="maroon")
ps10.pack(side=LEFT)
ps30 = Label(app, text="      ", font=helv24)
ps30.pack(side=LEFT)
ps100 = Button(app, text="VOL-", font=helv15, command=voldown, bg="pink", fg="maroon")
ps100.pack(side=LEFT)
ps300= Label(app, text="              ", font=helv24)
ps300.pack(side=LEFT)
ps1 = Button(app, text=u"\u2161", font=helv15, command=pause, bg="pink", fg="maroon")
ps1.pack(side=LEFT)
ps3 = Label(app, text="              ", font=helv24)
ps3.pack(side=LEFT)
ps0 = Button(app, text=u"\u25B6", font=helv15, command=unpause, bg="pink", fg="maroon")
ps0.pack(side=LEFT)
ps3 = Label(app, text="              ", font=helv24)
ps3.pack(side=LEFT)
ps2 = Button(app, text=u"\u25A0", font=helv15, command=stop, bg="pink", fg="maroon")
ps2.pack(side=LEFT)
ps3.pack(side=LEFT)
quit1 = Button(app, text=u"\u2718", font="Helvetica 18 bold italic", command=quit, bg="yellow", fg="maroon").pack(anchor=SE,side=BOTTOM)

app.mainloop()

