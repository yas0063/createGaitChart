import numpy as np
import datetime
import csv
import os

import tkinter as Tk
from tkinter import filedialog
#import matplotlib
#from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#from matplotlib.figure import Figure


class mainWindow:

    def __init__(self, nLegs_=6):

        self.nLegs = nLegs_
        self.legLabels = [""] * self.nLegs
        for i in range(int(self.nLegs/2)):
            self.legLabels[i] = "L"+str(i+1)
            self.legLabels[i+int(self.nLegs/2)] = "R"+str(i+1)

        self.shortcut_keys ={'a':0, 's':1, 'd':2, 'q':3, 'w':4, 'e':5}


        self.root = Tk.Tk()
        self.root.title(u"create gait chart")
        self.root.configure(width = 800, height=600, bg='gray60')
        self.root.grid()

        self.state = []
        self.checkboxes = []

        self.frame = 0
        self.frameTime = datetime.time()
        self.result = []

        for i in range(self.nLegs):
            self.state.append(Tk.BooleanVar())
            self.state[i].set(False)
        self.root.bind("<Key>", self.key_callback)
        self.root.bind("<Return>", self.return_callback)


        self.cXOffset = 50
        self.cYOffset = 30
        self.cfWidth = 800
        self.cfHeight = 350
        self.cdWidth = 720
        self.cdHeight = 300
        self.x_div = 20

        self.dispFrameNum = int(self.cdWidth/self.x_div) -1
        self.y_div = int(self.cdHeight/self.nLegs)


        self.canvas = Tk.Canvas(self.root, width = self.cfWidth, height = self.cfHeight, bg='gray60')
        self.canvas.grid(row=0, column=0, columnspan=8, padx=0, pady=0)
        self.canvas.create_rectangle(self.cXOffset, self.cYOffset, self.cXOffset+self.cdWidth, self.cYOffset+self.cdHeight, fill = 'white')

        self.updateGaitChart()

        self.createCheckboxes()
        self.createButtons()

        self.root.mainloop()

    def createCheckboxes(self):

        for i in range(self.nLegs):
            self.checkboxes.append(Tk.Checkbutton(text=self.legLabels[i], variable=self.state[i],command=self.updateDisp))

        self.cbLabel = Tk.Label(width=10, text='leg state',bg='gray30', fg='white')
        self.cbLabel.grid(row=2, column=1, columnspan=2,padx=1, pady=5)

        for i in range(int(self.nLegs/2)):
            # left legs
            self.checkboxes[i].grid(row=i+3,column=1, padx=5, pady=5)
            # right legs
            self.checkboxes[i+int(self.nLegs/2)].grid(row=i+3,column=2, padx=5, pady=5)


    def createButtons(self):

        self.button_prev = Tk.Button(self.root,text="prev",width=10,command=self.on_btn_prev_click)
        self.button_next = Tk.Button(self.root,text="next",width=10,command=self.on_btn_next_click)
        self.button_insert = Tk.Button(self.root,text="insert",width=10,command=self.on_btn_insert_click)
        self.button_delete = Tk.Button(self.root,text="delete",width=10,command=self.on_btn_delete_click)
        self.button_save = Tk.Button(self.root,text="save",width=10,command=self.on_btn_save_click)
        self.button_load = Tk.Button(self.root,text="load",width=10,command=self.on_btn_load_click)
        self.button_shutdown = Tk.Button(self.root,text="shutdowm",width=10,command=self.on_btn_shutdown_click)
        self.button_fset = Tk.Button(self.root,text="set",width=10,command=self.on_btn_fset_click)
        self.button_sset = Tk.Button(self.root,text="set/change",width=10,command=self.on_btn_sset_click)

        self.button_sset.grid(row=3,column=3, columnspan=1, padx=2, pady=10)
        self.button_insert.grid(row=4,column=3, columnspan=1, padx=2, pady=10)
        self.button_delete.grid(row=5,column=3, columnspan=1, padx=2, pady=10)

        self.button_prev.grid(row=4,column=5, columnspan=1, padx=2, pady=10, sticky=Tk.W)
        self.button_next.grid(row=4,column=5, columnspan=1, padx=2, pady=10, sticky=Tk.E)
        self.button_fset.grid(row=3,column=5, columnspan=1, padx=2, pady=10)

        self.lframe = Tk.Label(width=5, text='frame',bg='gray30', fg='white')
        self.lframe.grid(row=3, column=4, padx=1, pady=5, sticky=Tk.E)
        self.tframe = Tk.Entry(width=5)
        self.tframe.grid(row=3, column=5, padx=1, pady=5, sticky=Tk.W)

        self.ltime = Tk.Label(width=5, text='time',bg='gray30', fg='white')
        self.ltime.grid(row=5, column=4, padx=1, pady=5, sticky=Tk.E)
        self.ttime = Tk.Entry(width=20)
        self.ttime.grid(row=5, column=5, padx=1, pady=5, sticky=Tk.W)

        self.lmframe = Tk.Label(width=10, text='movie frame',bg='gray30', fg='white')
        self.lmframe.grid(row=6, column=4, padx=1, pady=5, sticky=Tk.E)
        self.tmframe = Tk.Entry(width=5)
        self.tmframe.grid(row=6, column=5, padx=1, pady=5, sticky=Tk.W)

        self.tframe.insert(Tk.END,str(self.frame))
        self.ttime.insert(Tk.END,self.frameTime.strftime("%H:%M:%S.%f"))
        self.tmframe.insert(Tk.END,'0')


        self.button_save.grid(row=3,column=6, columnspan=1, padx=2, pady=10)
        self.button_load.grid(row=4,column=6, columnspan=1, padx=2, pady=10)
        self.button_shutdown.grid(row=6,column=6, columnspan=1, padx=2, pady=10)


    def updateDisp(self):
        self.updateFrameNum()
        self.updateMovieFrameNum()
        self.updateTime()
        self.updateState()
        self.updateGaitChart()

    def updateMovieFrameNum(self):
        if not self.frame == len(self.result):
            self.tmframe.delete(0, Tk.END)
            self.tmframe.insert(Tk.END,str(self.result[np.clip(self.frame, 0, len(self.result))][2]))

    def updateFrameNum(self):
        self.tframe.delete(0, Tk.END)
        self.tframe.insert(Tk.END,str(self.frame))

    def updateTime(self):
        if not self.frame == len(self.result):
            self.ttime.delete(0, Tk.END)
            self.frameTime = datetime.datetime.strptime(self.result[np.clip(self.frame, 0, len(self.result))][1],"%H:%M:%S.%f")
            self.ttime.insert(Tk.END, self.frameTime.strftime("%H:%M:%S.%f"))

    def updateGaitChart(self):


        self.canvas.create_rectangle(0, 0, self.cfWidth, self.cfHeight, fill = 'gray60')
        self.canvas.create_rectangle(self.cXOffset, self.cYOffset, self.cXOffset+self.cdWidth, self.cYOffset+self.cdHeight, fill = 'white')#塗りつぶし


        dispStartFrame = np.clip(self.frame - self.dispFrameNum,0,self.frame)
        dispLastFrame = min(len(self.result), dispStartFrame + self.dispFrameNum+1)

        for f in range(dispStartFrame, dispLastFrame):
            for i in range(self.nLegs):
                xl = self.cXOffset+(f-dispStartFrame) * self.x_div
                xh = xl+self.x_div
                if self.result[f][i+3] == 1:
                    self.canvas.create_rectangle(xl, self.cYOffset+i*self.y_div, xh, self.cYOffset+(i+1)*self.y_div, fill = 'black')
                else:
                    self.canvas.create_rectangle(xl, self.cYOffset+i*self.y_div, xh, self.cYOffset+(i+1)*self.y_div, fill = 'white')

            self.canvas.create_text(xl+10,self.cYOffset+(i+1)*self.y_div+10, text=str(f),font=("Helvetica", 14), fill='white')

        for i in range(self.nLegs):
            xl = self.cXOffset+(self.frame-dispStartFrame) * self.x_div
            xh = xl+self.x_div
            if self.state[i].get() == True:
                    self.canvas.create_rectangle(xl, self.cYOffset+i*self.y_div, xh, self.cYOffset+(i+1)*self.y_div, fill = 'gray50')
            else:
                self.canvas.create_rectangle(xl, self.cYOffset+i*self.y_div, xh, self.cYOffset+(i+1)*self.y_div, fill = 'white')

            self.canvas.create_text(self.cXOffset/2,self.cYOffset+i*self.y_div+self.y_div/2, text=self.legLabels[i],font=("Helvetica", 18, "bold"), fill='white')


        xf = self.cXOffset+(self.frame - dispStartFrame)*self.x_div
        self.canvas.create_rectangle(xf, self.cYOffset, xf+self.x_div, self.cYOffset+self.cdHeight, outline = 'red', width = 2)
        self.canvas.create_text(xf+10,self.cYOffset+(i+1)*self.y_div+10, text=str(self.frame),font=("Helvetica", 14), fill='red')


    def appendNowState(self, insertMode=False):
        self.frameTime = datetime.datetime.strptime(self.ttime.get(),"%H:%M:%S.%f")
        tmp = [self.frame, self.frameTime.strftime("%H:%M:%S.%f"), int(self.tmframe.get())]
        for i in range(self.nLegs):
            if self.state[i].get() == True:
                tmp.append(1)
            else:
                tmp.append(0)

        if insertMode == True:
            self.result.insert(self.frame,tmp)
        elif len(self.result) > self.frame:
            self.result[self.frame] = tmp
        else:
            self.result.append(tmp)

    def updateState(self):
        if not self.frame == len(self.result):
            for i in range(self.nLegs):
                if self.result[self.frame][i+3] == 1:
                    self.state[i].set(True)
                else:
                    self.state[i].set(False)

    def on_btn_sset_click(self):
        self.appendNowState()
        self.frame = self.frame+1
        self.updateDisp()

    def on_btn_next_click(self):
        self.frame =  np.clip(self.frame+1, 0, len(self.result))
        self.updateDisp()

    def on_btn_fset_click(self):
        self.frame = np.clip(int(self.tframe.get()), 0, len(self.result))
        self.updateDisp()

    def on_btn_prev_click(self):
        self.frame = np.clip(self.frame-1, 0, len(self.result))
        self.updateDisp()


    def on_btn_save_click(self):
        iDir = os.path.abspath(os.path.dirname(__file__))
        filename =  Tk.filedialog.asksaveasfilename(initialdir = iDir,title = "Save as",filetypes =  [("text file","*.csv")])
        if not filename == "":
            with open(filename, 'w') as file:
                writer = csv.writer(file, lineterminator='\n')
                writer.writerows(self.result)

    def on_btn_load_click(self):
        iDir = os.path.abspath(os.path.dirname(__file__))
        filename =  Tk.filedialog.askopenfilename(initialdir = iDir,title = "Load as",filetypes =  [("text file","*.csv")])
        if not filename == "":
            with open(filename, 'r') as file:
                reader = csv.reader(file)
                data = [row for row in reader]

        if not data == []:
            self.result=[]
            for i in range(len(data)):
                tmp=[int(data[i][0])]  # frame num
                tmp.append(data[i][1]) # time 
                tmp.append(int(data[i][2])) # movie frame num
                for n in range(self.nLegs):
                    tmp.append(int(data[i][n+3]))
                self.result.append(tmp)
        self.updateDisp()

    def on_btn_insert_click(self):
        self.appendNowState(True)
        self.frame = self.frame+1
        self.updateDisp()

    def on_btn_delete_click(self):
        if not self.frame == len(self.result):
            self.result.pop(self.frame)
            self.updateDisp()

    def on_btn_shutdown_click(self):
        self.root.quit()

    def toggle_state(self,s):
        if s.get() == True:
            s.set(False)
        else:
            s.set(True)

    def key_callback(self, event):
        key = event.keysym
        if key in self.shortcut_keys.keys():
            self.toggle_state(self.state[self.shortcut_keys[key]])
        elif key == 'n':
            self.on_btn_next_click()
        elif key == 'b':
            self.on_btn_prev_click()
        elif key == 'f':
            self.on_btn_sset_click()
        elif key == 'h':
            self.on_btn_sset_click()
        self.updateGaitChart()

    def return_callback(self, event):
        self.ltime.focus_set()


import sys

if __name__ == "__main__":

    args = sys.argv
    if len(args) > 1 :
        app = mainWindow(int(args[1]))
    else:
        app = mainWindow()