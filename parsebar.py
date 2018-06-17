#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python

import sys
import serial
from blessings import Terminal
from progressive.bar import Bar


if len(sys.argv) == 1:
    print("1st arg: serial port e.g. : /dev/tty. device ")
    print("2nd arg: parse string e.g. : \'$A1:\'")
    print("3rd arg: max value for bar e.g. : 4095")

ser = serial.Serial(sys.argv[1])

print sys.argv
arg = sys.argv[1:]


bar = []
bar.append(Bar(title=arg[1].ljust(10), max_value=int(arg[2]), fallback=True))
bar[0].cursor.clear_lines(len(arg)/2 +3)
bar[0].cursor.save()

title = []
title.append(arg[1])

for i in range(3, len(arg)-1, 2):
    bar.append(Bar(title=arg[i].ljust(10), max_value=int(arg[i+1]), fallback=True))
    title.append(arg[i])
    #print("title: " + arg[i] + " max: " + arg[i+1])

val = []
for i in range(len(arg)/2):
    val.append(0)

while True:
    if ser.readable:
        line = ser.readline()
        bar[0].cursor.restore()

        for i, t in enumerate(title):
            if t in line:
                val[i] = line[len(t):-1]                

        for i, v in enumerate(val):
            #print("Val" + str(i) + ": " + str(v))
            bar[i].draw(value=int(v))
