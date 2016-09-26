# change this shit so the receiver is constantly adding to the queue and the reader is constantly popping from the queue and checking if the string would serve as a message,
# remove that message from the string, then process it.
# pretty sure just have to change the line in reader to stop reading from goo when eom bits are received and have receiver keep adding to queue
# fuck i am a lazy-assed motherfucker right now
import threading
import queue
import time
import random

import receiveblinks as client
from SetPin import SetPin

Q1=queue.Queue(100)  #100 limits number of inputs from foo that can be Queued.

def mainThread():
    h=threading.Thread(target=receiver,name="HIGHER")
    # note that "goo" is started by "for I in goo()" in function "hoo"
    # goo reads queued items from foo and yields them to hoo
    f=threading.Thread(target=reader,name="LOWER")
    print("STARTING")
    h.start()
    f.start()
    f.join()
    h.join()

def reader():
    while(True):
        message = ''
        new = True
        for I in goo():
            if(I and new):
                print('Message received!')
                new = False
            message += '.' if I else '*'
            if(message.find('.' * 8) != -1 or (message[len(message) - 1] == '*' and message[len(message) - 7:len(message) - 1] == '......')):
                if(message[len(message) - 1] == '*' and message[len(message) - 7:len(message) - 1] == '......'):
                    message = message[:len(message) - 7]  + '.' * 8
                break
        print('Proccessing...')
        start = message.find('.')
        if(start == -1):
            pass
        else:
            try:
                print(client.process(message[start:]))
                print('Ready for next message')
            except Exception:
                print('Error reading message, please try again')
                print(message[start:])

def goo():
    # "gets values from Q1 queue; foo puts values onto Q1 queue"
    while True:
        g = Q1.get()
        if g != "/":
            yield g
        else:
            break

def receiver(): #receives from physical layer
    duration = .02
    with SetPin(16, 'GPIO_23', direction='RX') as RXpin:
        while True:
            Q1.put(RXpin.read_pin())
            time.sleep(duration)

if __name__ == "__main__":
    mainThread()
