from typing import Iterator
from concurrent.futures import ThreadPoolExecutor

def _next_iter(iter):
    return next(iter)

def threaded_iterator(iter):
    with ThreadPoolExecutor() as e:
        f = e.submit(_next_iter, iter)
        while True:
            try:
                n = f.result()
            except StopIteration:
                break
            f = e.submit(_next_iter, iter)
            yield n

if __name__ == "__main__":
    import time

    def rand_gen(n=5):
        import random
        for _ in range(n):
            time.sleep(1)
            yield random.random()
    
    start = time.time()
    for r in rand_gen():
        time.sleep(1)
        print(r, end=",")
    print()
    print(time.time()-start)
    

    start = time.time()
    for r in threaded_iterator(rand_gen()):
        time.sleep(1)
        print(r, end=",")
    print()
    print(time.time()-start)
    