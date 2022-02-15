import multiprocessing as mp
import time

def worker():
    proc = mp.current_process()
    print(proc.name,proc.pid)
    time.sleep(5)
    print("SubProcess End")

if __name__== "__main__":
    # main
    proc = mp.current_process()
    print(proc.name,proc.pid)

    # spawning
    p = mp.Process(name="SubProcess",target=worker)
    p.start()

    print("MainProcess End")