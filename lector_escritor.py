
from threading import Lock, Thread, currentThread
import time

lock = Lock()


def escritor(lock):
    while True:
        have_it = lock.acquire()
        try:
            if have_it:
                print('El ', currentThread().getName(), "accedió a la BD")
                time.sleep(3)
            else:
                print(currentThread().getName(), "intentó acceder")
        finally:
            print(currentThread().getName(), 'dejó de usar bd')
            lock.release()

        time.sleep(0.5)


def lector(lock):
    while True:
        have_it = lock.acquire()
        try:
            if have_it:
                print('El ', currentThread().getName(), "accedió a la BD")
                time.sleep(3)
            else:
                print(currentThread().getName(), "intentó acceder")
        finally:
            print(currentThread().getName(), 'dejó de usar bd')
            lock.release()

        time.sleep(0.5)



t1 = Thread(target=escritor, args=(lock,), name='Escritor')

t2 = Thread(target=lector, args=(lock,), name='Lector')
t1.start()
t2.start()
