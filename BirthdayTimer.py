from tkinter import *
from tkinter import Tk, Toplevel, Label, messagebox
from tkinter import ttk
import sqlite3
from datetime import datetime
root = Tk()
root.configure(bg="#dcdad5")
root.overrideredirect(True)
root.tk.call('tk','scaling',0.7)
root.attributes("-topmost",True)
ViewVar=True
s = ttk.Style()
s.theme_use("clam")
def moveable(win):
    def start_move(event):
        win.x=event.x
        win.y=event.y
    def domove(event):
        dax = event.x-win.x
        day = event.y-win.y
        x= win.winfo_x()+dax
        y=win.winfo_y()+day
        win.geometry(f"+{x}+{y}")

    win.bind("<Button-1>", start_move)
    win.bind("<B1-Motion>", domove)
def SettingsWindow(event):

    global SettingsWin
    SettingsWin = Toplevel(root)
    SettingsWin.tk.call('tk','scaling',1.5)
    SettingsWin.attributes("-topmost",True)
    SettingsWin.title("Settings")
    SettingsWin.overrideredirect(True)
    SettingsWin.configure(bg="#dcdad5")
    ttk.Label(SettingsWin, text = "Slider for no reason:").pack(pady=10)
    Scalevar=DoubleVar(value=Scale if 'scale' in globals() else 1.0)
    Scaley=ttk.Scale(SettingsWin,from_=0.5,to=3.0,orient=HORIZONTAL,variable=Scalevar)
    Scaley.pack(padx=10)
    def apply():
        global scale
        scale=Scalevar.get()
        root.tk.call('tk','scaling',scale)
        SettingsWin.destroy()

    ttk.Button(SettingsWin, command=apply, text="Apply").pack()
    moveable(SettingsWin)
    SettingsWin.bind("<Button-3>",lambda event: SettingsWin.destroy())
def Buttonbutton(event=None):
    global ViewVar
    ViewVar = not ViewVar
def Timer():
    connection = sqlite3.connect("Birthday.db")
    if connection:
        print("Aha")
    else:
        print("Nahah")
    c = connection.cursor()
    c.execute("SELECT month, day FROM BirthdayTable")
    birthdays =c.fetchall()
    connection.close()

    now = datetime.now()
    if not birthdays:
        Countdown.config(text="No Bday in DB")
    else:
        countdowntext = " "
        for month, day in birthdays:
            targetdate = datetime(now.year,month,day)
            if targetdate < now:
                targetdate = datetime(now.year+ 1, month,day)
            remaining=targetdate-now
            days=remaining.days
            seconds=remaining.seconds
            hours=(seconds //3600)
            minutes= (seconds %3600)//60
            seconds = seconds % 60
            if  ViewVar:
                countdowntext =f"{days}d {hours}h {minutes}m {seconds}s\n"
            else:
                if days>0:
                    countdowntext = f"{days} day(s)"
                elif hours>0:
                    countdowntext = f"{hours} hour(s)"
                elif minutes>0:
                    countdowntext = f"{minutes} minute(s)"
                else:
                    countdowntext = f"{seconds} second(s)"
        Countdown.config(text=countdowntext)
    Countdown.after(1000, Timer)

def initdb():
    connection= sqlite3.connect("Birthday.db")
    if connection:
        print("Aha")
    else:
        print("Nahah")
    c = connection.cursor()
    c.execute("create table if not exists BirthdayTable(month integer,day integer)")
    connection.commit()
    connection.close()
def dateinput(event):
    global BDayWindow
    BDayWindow = Toplevel(root)
    BDayWindow.tk.call('tk','scaling',1.5)
    BDayWindow.title("Birthday Enter :)")
    BDayWindow.overrideredirect(True)
    BDayWindow.configure(bg="#dcdad5")
    EnterYourBday=ttk.Label(BDayWindow,text="Enter your Birthday",font="Arial 20")
    EnterYourBday.grid(column=0,row=0,columnspan=4)
    DayLabel=ttk.Label(BDayWindow,text="Day:")
    DayLabel.grid(column=0,row=1)
    MonthLabel=ttk.Label(BDayWindow,text="Month:")
    MonthLabel.grid(column=2,row=1)
    DaEntry = ttk.Entry(BDayWindow, textvariable=Daytextvar,width=2)
    DaEntry.grid(column = 1,row=1)
    MoEntry = ttk.Entry(BDayWindow, textvariable=Monthtextvar,width=2)
    MoEntry.grid(column=3,row=1)
    s = ttk.Style()
    s.configure("Green.TButton",background = "#90ee90",font = ("Arial", 12,"bold"))
    s.map("Green.Tbutton",background=[("active","7ccd7c")])
    EnterButton= ttk.Button(BDayWindow, text="Submit",command=SubmitButton,style= "Green.TButton")
    EnterButton.grid(column=1,columnspan=2,row=2,pady=10)
    moveable(BDayWindow)
def SubmitButton():
    Month=Monthtextvar.get()
    Day=Daytextvar.get()
    if Month.isdigit() and len(Month)==2 and Day.isdigit() and len(Day)==2:
        connection = sqlite3.connect("Birthday.db")
        if connection:
            print("Aha")
        else:
            print("Nahah")
        c = connection.cursor()
        c.execute("DELETE FROM BirthdayTable")
        c.execute("insert into BirthdayTable (month, day) values (?,?)",(int(Month),int(Day)))
        connection.commit()
        connection.close()
        BDayWindow.destroy()
    else:
        messagebox.showerror("Date Error","Please make sure that you enter 2 numbers for each entry, for example"
                                          " 9th of september would be 09 09.")
def HoverHide(win):
    def hide(event):
        win.withdraw()
    def show(event):
        win.deiconify()
        win.lift()
        win.focus_force()
    win.bind("<Enter>",hide)
    win.bind("<Leave>",show)
initdb()

Daytextvar=StringVar()
Monthtextvar=StringVar()
root.title("Birthday timer!!")

TitleFrame=Frame(root)
TitleFrame.pack()
Title=ttk.Label(TitleFrame, text = "Birthday Timer!", font="Arial 10 bold")
Title.grid()

CountDownFrame = Frame(root)
CountDownFrame.pack()
Countdown = ttk.Label(CountDownFrame, text="Initialising",font= "Arial 40 bold")
Countdown.grid()

# BellowFrame = Frame(root)
# BellowFrame.pack()
# ViewButton = ttk.Button(BellowFrame,text="Change view",command=Buttonbutton)
# ViewButton.pack()
moveable(root)
root.bind("<Control-Shift-S>",dateinput)
root.bind("<Control-Shift-V>",Buttonbutton)
root.bind("<Control-Shift-I>",SettingsWindow)
root.bind("<Button-3>",lambda event: root.destroy())
# HoverHide(root)
Timer()
root.mainloop()