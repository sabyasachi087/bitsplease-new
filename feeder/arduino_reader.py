import os.path as osp
from feeder.SerialReader import SerialReader
import sys
from messaging.mq_writer import TestDataMessageWriter
import random

FOLDER_SPACE = "data/"


def start():
    while True:
        cmd = input('Enter T for train ,P for Predict type anything else to exit : ')
        processCmd(cmd)


def train():
    word = input('Enter the word for training : ')
    while True:
        cmd = input('Press enter to start or "e" to exit : ')
        if cmd == '':
            rdr = SerialReader(1, "Reader-Thread", 1)
            rdr.start()
            input('Press enter to stop : ')
            data = rdr.stop()
            storeData(word, data)
        elif cmd == 'e':
            break;


def predict():
    tid = random.randint(1, 100)
    mq_writer = TestDataMessageWriter(tid, 'test_writer')
    mq_writer.start()
    input('Device Writer Started , press enter to exit : ')
    mq_writer.stop()
    

def processCmd(cmd):
    if cmd.upper() == 'T':
        train()
    elif cmd.upper() == 'P':
        predict()
    else:
        print('Exiting ...  ')
        sys.exit()          


def storeData(word, data):
    filename = "_".join(word.split()) 
    file = open(FOLDER_SPACE + osp.sep + filename + '.txt', 'a+', 1024)
    for dp in data:
        file.write(dp.decode('utf-8', 'ignore'))
    file.write("---------END--------\n")
    file.close()


if __name__ == "__main__":
    start()
