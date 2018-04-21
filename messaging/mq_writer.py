import threading
import serial
import stomp
import random
import json


class TestDataMessageWriter(threading.Thread):

    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.exit = False
        self.ser = serial.Serial('/dev/ttyACM0', 9600)
        self.dest = '/queue/gest.recg.test.queue'
        self.temp = []
        self._init_conn()
    
    def _init_conn(self):
        self.conn = stomp.Connection()       
        self.conn.start()
        self.conn.connect('admin', 'admin', wait=True)
#         self.conn.subscribe(destination='/queue/gest.recg.test.queue', id=1, ack='auto')
    
    def stop(self):
        self.exit = True

    def run(self):
        count = random.randint(20, 35)
        while not self.exit:
            if count == 0:
                self.storetoMQ(self.temp)
                self.temp = []
                count = random.randint(25, 41)
            else:
                dp = self.ser.readline()
                self.temp.append(dp.decode('utf-8', 'ignore'))
                count = count - 1
        self.ser.close()   
        self.conn.disconnect()

    def storetoMQ(self, datax):
        finalstring = "__".join(datax)
        self.conn.send(body=finalstring, destination=self.dest)
