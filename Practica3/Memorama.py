"""
    bibliotecas
"""
from random import random
import logging

FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] (%(threadName)-2s) %(message)s"
logging.basicConfig(level=logging.DEBUG,
                    format=FORMAT)

class Memorama:

    def __init__(self, nivel):
        self.nivel = nivel
        self.tablero = []
        logging.debug("Memorama creado")

    def leer_cartas(self):
        with open("lista_palabras.txt") as file_palabras:
            cartas = file_palabras.readlines()
            if self.nivel == "principante":
                cartas = cartas[:16]
            if self.nivel == "avanzado":
                cartas = cartas[:36]
        return cartas

    def revolver_cartas(self, cartas):
        cartas = random.shuffle(cartas)
        return cartas

    # Recibe arreglo de las coordenadas de la carta
    def voltear_carta(self, cartas):
        logging.debug("Voltea las cartas recibidas")
        respuesta = []
        respuesta["palabra1"] = self.tablero[cartas["x1"]][cartas["y1"]]
        respuesta["palabra2"] = self.tablero[cartas["x2"]][cartas["y2"]]
        return respuesta

    def compara_cartas(self, cartas):
        return self.tablero[cartas["x1"]][cartas["y1"]] == self.tablero[cartas["x2"]][cartas["y2"]]


    



