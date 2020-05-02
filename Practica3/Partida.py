import threading
import Memorama
import logging

FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] (%(threadName)-2s) %(message)s"
logging.basicConfig(level=logging.DEBUG,
                    format=FORMAT)

class Partida:

    def __init__(self, jugador, tipo_partida, nivel, no_jugadores = 2):
        self.id_partida = None # Identificador de la partida
        self.no_jugadores = no_jugadores
        self.nivel = nivel
        self.barrier_jugadores = threading.Barrier(int(no_jugadores))
        self.jugadores = []
        self.marcador = []
        self.jugadores.append(jugador)
        self.tipo_partida = tipo_partida
        self.turno = 0
        self.memorama = Memorama.Memorama(nivel)

        self.marcador = [0 for x in range(int(no_jugadores))]

    # Recibe el identificador de un hilo
    def agregar_jugador(self, jugador):
        if len(self.jugadores) <= self.no_jugadores:
            self.jugadores.append(jugador)
            logging.debug("Jugador agregado a la partida %s", self.id_partida)
        else:
            logging.debug("Ya hay suficientes jugadores en la partida %s", self.id_partida)

    def empezar_partida(self, jugador):
        logging.debug('Esperando en la barrera con %s hilos más', format(self.barrier_jugadores.n_waiting))
        self.jugadores.append(jugador)
        worker_id = self.barrier_jugadores.wait()
        self.no_jugadores = worker_id
        logging.debug('Después de la barrera %s', worker_id)
        logging.debug("Jugadores completos para la partida %s", self.id_partida)

    def get_id_partida(self):
        return self.id_partida

    def get_no_jugadores(self):
        return self.no_jugadores

    def get_lugares_disponibles(self):
        return self.no_jugadores - len(self.jugadores)

    def agregar_punto_jugador(self, jugador):
        self.marcador[jugador] += self.marcador[jugador]

    def set_id_partida(self, id_partida):
        self.id_partida = id_partida

    def cambiar_turno(self):
        if self.turno >= len(self.jugadores):
            self.turno = 0
        logging.debug("Asignar jugada a %s", self.jugadores[self.turno])
        self.turno += 1

    def get_turno(self):
        return self.turno

    def jugada(self, jugador, cartas):
        logging.debug("")
        respuesta = []
        if self.memorama.comparar_cartas(cartas):
            respuesta = self.memorama.voltear_cartas(cartas)
            self.agregar_punto_jugador(jugador)
        else:
            self.cambiar_turno()

        return respuesta
