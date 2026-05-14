PROVIDES = [ "WorkerInfo" ]

import threading, queue
import multiprocessing as mp

backend = mp # <--- mp or threading

import time

QUEUE = mp.Queue() if backend is mp else queue.Queue()
STOP = backend.Event()
THREAD = backend.Process() \
            if backend is mp else backend.Thread()

def _init():
    THREAD._target = worker_loop
    THREAD._args = (QUEUE,)
    THREAD.start()
    print("Worker started.")

def _update(bb):
    QUEUE.put("Hello Queue!")
    time.sleep(0.5)

def worker_loop(q):
    while not STOP.is_set():
        while not q.empty():
            print("Worker has msg:")
            print(q.get())

def _close():
    STOP.set()
    if THREAD is not None:
        THREAD.join()

    print("Worker stopped cleanly.")

