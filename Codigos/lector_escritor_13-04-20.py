import logging
import threading
import time

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-2s) %(message)s')


class Taller(object):
    def __init__(self, start=0):
        self.condicionMangasMAX = threading.Condition()
        self.condicionCuerposMAX = threading.Condition()
        self.condicionMangasMIN = threading.Condition()
        self.condicionCuerposMIN = threading.Condition()
        self.mangas = 0
        self.cuerpos = 0
        self.prendas_completas = 0
        # prenda

    def incrementarManga(self):
        with self.condicionMangasMAX:
            if self.mangas >= 10:
                logging.debug("No hay espacio para mangas")
                self.condicionMangasMAX.wait()
            else:
                self.mangas += 1
                logging.debug("Manga creada, mangas=%s", self.mangas)
        with self.condicionMangasMIN:
            if self.mangas >= 2:
                logging.debug("Existen suficientes mangas")
                self.condicionMangasMIN.notify()

    def decrementarManga(self):
        with self.condicionMangasMIN:
            while not self.mangas >= 2:
                logging.debug("Esperando mangas")
                self.condicionMangasMIN.wait()
            self.mangas -= 2
            logging.debug("Mangas tomadas, mangas=%s", self.mangas)
        with self.condicionMangasMAX:
            logging.debug("Hay espacio para mangas")
            self.condicionMangasMAX.notify()

    def getMangas(self):
        return (self.mangas)

    def getCuerpos(self):
            return (self.cuerpos)

    def decrementarCuerpo(self):
        with self.condicionCuerposMIN:
            while not self.cuerpos >= 1:
                logging.debug("Esperando cuerpos")
                self.condicionCuerposMIN.wait()
            self.cuerpos -= 1
            logging.debug("Cuerpo tomado, cuerpos=%s", self.cuerpos)
        with self.condicionCuerposMAX:
            logging.debug("Hay espacio para cuerpos")
            self.condicionCuerposMAX.notify()

    def incrementarCuerpo(self):
        with self.condicionCuerposMAX:
            # verificar que la cesta de cuerpos no esté llena
            if self.cuerpos >= 5:
                logging.debug("Cesta de cuerpos llena")
                self.condicionCuerposMAX.wait()
            else:
                self.cuerpos += 1
                logging.debug("Cuerpo creado, cuerpos=%s", self.cuerpos)
        with self.condicionCuerposMIN:
           if self.cuerpos >= 1:
                # notificar que hay cuerpos disponibles
                logging.debug("Existen suficientes cuerpos")
                self.condicionCuerposMIN.notify()

    def incrementarPrenda(self):
        self.prendas_completas += 1
        logging.debug("Prenda creada, prenda=%s", self.prendas_completas)


def crearManga(Taller):
    while (Taller.getMangas() <= 10):
        Taller.incrementarManga()
        time.sleep(5)


def crearCuerpo(Taller):
    while (Taller.getMangas() >= 0):
        # incrementarCuerpo (antes de decrementar
        # manga se debe validar que haya cupo en
        # la canasta de cuerpos)
        while(Taller.getCuerpos() <= 5):
            Taller.decrementarManga()
            Taller.incrementarCuerpo()
            time.sleep(1)


def ensamblaPrenda(Taller):
    while (Taller.getCuerpos() >= 0):
        Taller.decrementarCuerpo()
        Taller.incrementarPrenda()


taller = Taller()
Lupita = threading.Thread(name='Lupita(mangas)', target=crearManga, args=(taller,))
Sofia = threading.Thread(name='Sofía(cuerpos)', target=crearCuerpo, args=(taller,))
Luis = threading.Thread(name='Luis(ensamble)', target=ensamblaPrenda, args=(taller,))
Lupita.start()
Sofia.start()
Luis.start()
Lupita.join()
Sofia.join()
Luis.join()

