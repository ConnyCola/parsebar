import sys
from serial import *
from Tkinter import *
from tkinter import ttk

arg = sys.argv[2:]

serialPort = sys.argv[1]
serialPort = "/dev/tty.wchusbserial1410"
baudRate = 115200
ser = Serial(serialPort , baudRate, timeout=0, writeTimeout=0) #ensure non-blocking

#make a TkInter Window
root = Tk()
root.wm_title("Reading Serial")

lab_array = []
progress_array = []
search_array = []

for i in range(len(arg)/2):
    print "generate " + str(arg[i*2])
    l = Label(root, text="", font= "Helvetica 16")
    pb = ttk.Progressbar(root, orient='horizontal', mode='determinate', length=500)
    pb["maximum"] = int(arg[i*2+1])
    lab_array.append(l)
    progress_array.append(pb)
    search_array.append(str(arg[i*2]))
    l.pack()
    pb.pack()


#make our own buffer
#useful for parsing commands
#Serial.readline seems unreliable at times too
serBuffer = ""

def readSerial():
    while True:
        c = ser.read() # attempt to read a character from Serial
        
        #was anything read?
        if len(c) == 0:
            break
        
        # get the buffer from outside of this function
        global serBuffer
        
        # check if character is a delimeter
        if c == '\r':
            c = '' # don't want returns. chuck it
            
        if c == '\n':
            serBuffer += "\n" # add the newline to the buffer
            
            #add the line to the TOP of the log
            #log.insert('0.0', serBuffer)
            # try:
            #     lab_array[int(serBuffer[2])-1].configure(text=serBuffer)
            #     progress_array[int(serBuffer[2])-1]["value"] = serBuffer[4:]
            # except:
            #     pass

            for i, s in enumerate(search_array):
                if s in serBuffer:
                    try:
                        lab_array[i].configure(text=serBuffer)
                        progress_array[i]["value"] = serBuffer[len(s):]
                    except:
                        print "Error"
                        pass


            serBuffer = "" # empty the buffer
        else:
            serBuffer += c # add to the buffer
    
    root.after(10, readSerial) # check serial again soon


# after initializing serial, an arduino may need a bit of time to reset
root.after(100, readSerial)

root.mainloop()
