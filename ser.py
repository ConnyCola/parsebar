import sys
from serial import *
from tkinter import *
from tkinter import ttk
import matplotlib
# matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
#import numpy as np
import time

arg = sys.argv[2:]

serialPort = sys.argv[1]
serialPort = "/dev/tty.wchusbserial1410"
baudRate = 115200
ser = Serial(serialPort, baudRate, timeout=0, writeTimeout=0)  # ensure non-blocking

# make a TkInter Window
root = Tk()
root.wm_title("Reading Serial")

lab_array = []
progress_array = []
search_array = []
num_array = range(500)
va = range(500)
value_array = []

plot_array = []

# print arg

for i in range(len(arg) / 2):
    print("generate " + str(arg[i * 2]))
    l = Label(root, text="", font="Helvetica 16", width=13)
    pb = ttk.Progressbar(root, orient='horizontal', mode='determinate', length=500)
    pb["maximum"] = int(arg[i * 2 + 1])
    lab_array.append(l)

    value_array.append(va)

    progress_array.append(pb)
    search_array.append(str(arg[i * 2]))
    # put widgets in grid
    l.grid(row=i, column=0)
    pb.grid(row=i, column=1)

    plt.subplot((100 * len(arg) / 2 + 100) + 11 + i)
    plt.axis([0, 500, 0, int(arg[i * 2 + 1])])
    p, = plt.plot([], [])
    plot_array.append(p)


# make our own buffer
# useful for parsing commands
# Serial.readline seems unreliable at times too
serBuffer = ""


def readSerial():

    while True:
        c = ser.read()  # attempt to read a character from Serial

        # was anything read?
        if len(c) == 0:
            break

        # get the buffer from outside of this function
        global serBuffer
        global value_array
        # check if character is a delimeter
        if c == '\r':
            c = ''  # don't want returns. chuck it

        if c == '\n':
            serBuffer += "\n"  # add the newline to the buffer

            for i, s in enumerate(search_array):
                if s in serBuffer:
                    try:
                        v = serBuffer[len(s):]
                        lab_array[i].configure(text=serBuffer)
                        progress_array[i]["value"] = v

                        v = int(float(v))
                        value_array[i] = value_array[i][1:]
                        value_array[i].append(v)

                    except:
                        print("Error")
                        pass

            serBuffer = ""  # empty the buffer
        else:
            serBuffer += c  # add to the buffer
    # plt.show()

    root.after(10, readSerial)  # check serial again soon


def updatePlot():
    global num_array
    global value_array
    global plot_array

    for i, p in enumerate(plot_array):
        p.set_ydata(value_array[i])
        p.set_xdata(num_array)

    plt.pause(0.001)
    root.after(30, updatePlot)  # check serial again soon


# after initializing serial, an arduino may need a bit of time to reset

root.after(100, readSerial)
root.after(200, updatePlot)
root.geometry("650x" + str(root.winfo_reqheight()))

root.mainloop()
