#!/usr/bin/env python

import threading

class PCMonitor:
    """
    Producer-Consumer Monitor
    """
    
    def __init__(self):
        self.buffer=list() # Infinite buffer
        self.lock=threading.Lock() # Lock
        self.CV=threading.Condition(self.lock) # Condition variable

    def produce(self):
        # Wait
        self.lock.acquire()
        
        # Critical section
        print("P",end="")
        self.buffer.append(0)

        # Notify
        self.CV.notify()
        self.lock.release()

    def consume(self):
        # Wait
        self.lock.acquire()
        while(len(self.buffer)<=0):
            print("W",end="")
            self.CV.wait()

        # Critical section
        print("C",end="")
        self.buffer.pop() # Consume

        # Exit
        self.lock.release()


def ProducerThread(mon):
    for i in range(0,99):
        mon.produce()
        
def ConsumerThread(mon):
    for i in range(0,100):
        mon.consume()


# Instantiate monitor
mon=PCMonitor()

# Instantiate threads (producers and consumers)
threads=list()
for i in range(0,50): # Set number of threads here
    threads.append(threading.Thread(name="Thread-"+str(i), target=ProducerThread, args=[mon]))
    threads.append(threading.Thread(name="Thread-"+str(i), target=ConsumerThread, args=[mon]))

# Start threads
for t in threads:
    t.start()

# Join threads
for t in threads:
    t.join()
