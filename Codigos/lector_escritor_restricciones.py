from threading import Lock, Thread, currentThread, Barrier
import time

lock = Lock()

dato = "Hola"


NUM_ESCRITORES = 2

barrier = Barrier(NUM_ESCRITORES)

class Counter(object):
    def __init__(self, start=0):
        self.lock = Lock()
        self.value = start

    def increment(self):
        #logging.debug('Esperando por el candado')
        self.lock.acquire()
        try:
            #logging.debug('Candado adquirido')
            self.value = self.value + 1
        finally:
            self.lock.release()

def escritor(lock, barrier, cont):
    global dato

    print(currentThread().name, 'Esperando en la barrera con {} hilos más'.format(barrier.n_waiting))
    worker_id = barrier.wait()
    print(currentThread().name, "Después de la barrera", worker_id)

    while True:
        have_it = lock.acquire()
        try:
            if have_it:
                print('El ', currentThread().getName(), "accedió a la BD")
                print(currentThread().getName(), "- Valor anterior de la variable: ", dato)

                cont.increment()

                dato = dato + " " + str(cont.value)
                print(currentThread().getName(), "- Valor nuevo: ", dato)
                time.sleep(5)
            else:
                print(currentThread().getName(), "intentó acceder")
        finally:
            print(currentThread().getName(), 'dejó de usar bd')
            lock.release()

        time.sleep(0.5)


def lector(lock):
    global dato
    while True:
        have_it = lock.acquire()
        try:
            if have_it:
                print('El ', currentThread().getName(), "accedió a la BD")
                print(currentThread().getName(), "- La información de dato es: ", dato)
                time.sleep(3)
            else:
                print(currentThread().getName(), "intentó acceder")
        finally:
            print(currentThread().getName(), 'dejó de usar bd')
            lock.release()

        time.sleep(0.5)


cont = Counter()

t1 = Thread(target=escritor, args=(lock, barrier, cont), name='Escritor 1')
t4 = Thread(target=escritor, args=(lock, barrier, cont), name='Escritor 2')

t2 = Thread(target=lector, args=(lock, ), name='Lector 1')
t3 = Thread(target=lector, args=(lock, ), name='Lector 2')

t1.start()
time.sleep(1)
t2.start()
time.sleep(1)
t3.start()
time.sleep(1)
t4.start()
time.sleep(1)

