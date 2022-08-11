import random
import threading
import multiprocessing
import logging
from threading import Thread
from queue import Queue # used to share data between processes
import time
logging.basicConfig(format="%(levelname)s - %(asctime)s.%(msecs)03d: %(message)s", datefmt="%H:%M:%S",level=logging.DEBUG)

# show the processName, threadName and msg
def display(msg):
    threadName = threading.current_thread().name
    processName = multiprocessing.current_process().name
    logging.info(f'{processName}\{threadName}: {msg}')

# producer 
def createWork(queue, finished, max):
    finished.put(False) # queue work as FIFO
    for x in range(max):
        v = random.randint(1, 100)
        queue.put(v)
        display(f'Producing {x}: {v}')
    finished.put(True)
    display('finished')

# consumer
def performWork(work, finished):
    counter = 0
    while True:
        if not work.empty():
            v = work.get()
            display(f'Consuming {counter}: {v}')
            counter += 1
        else: 
            q = finished.get()
            if q == True:
                break
        display("finished")

def main():
    max = 50
    work = Queue()
    finished = Queue()

    producer = Thread(target=createWork, args=[work, finished, max], daemon=True)
    consumer = Thread(target=performWork, args=[work, finished], daemon=True)

    producer.start()
    consumer.start()

    producer.join()
    display('Producer has finished')

    consumer.join()
    display("Consumer has finished")

    display('Finished')


if __name__ == "__main__":
    main()