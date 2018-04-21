import threading
import serial 


class SerialReader (threading.Thread):

    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.exit = False
        self.ser = serial.Serial('/dev/ttyACM0', 9600)
        self.data = []
    
    def stop(self):
        self.exit = True
        return self.data
        
    def run(self):
        while not self.exit:
            self.data.append(self.ser.readline())
        self.ser.close()
        
