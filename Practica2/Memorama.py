import random
import numpy as np
import time



class Memorama(object):
    #Variables globales
    def __init__(self):
        self.turno = 0 #0 -> usuario, 1 -> servidor
        self.size = 0
        self.tablero = []
        self.tablero_deamentis = []
        self.tablero_marca = []
        self.usuario = 0
        self.servidor = 0
        self.bandera1 = 0
        self.bandera2 = 0

    def leer_palabras(self, nivel):
        with open("lista_palabras.txt") as file_palabras:
            palabras = file_palabras.readlines()        
        #verificamos el nivel del juego para el tamaño del self.tablero
        if nivel == "principiante":
            palabras = palabras[:16]
            self.size = 4
        if nivel == "avanzado":
            palabras = palabras[:36]
            self.size = 6

        random.shuffle(palabras)
        return palabras

    def compara_tarjetas(self, row1, col1, row2, col2):


        if (self.tablero[row1][col1] == self.tablero[row2][col2]):
            self.tablero_marca[row1][col1] = 1
            self.tablero_marca[row2][col2] = 1
            if(self.consultar_turno() == 1):
                self.servidor = self.servidor + 1
                self.asignar_turno(1)
            else:
                self.usuario = self.usuario + 1
                self.asignar_turno(0)
            return True
        else:
            if(self.consultar_turno() == 1):
                self.asignar_turno(0)
            else:
                self.asignar_turno(1)
            if(self.bandera1 == 0):
                self.tablero_marca[row1][col1] = 0
            if(self.bandera2 == 0):
                self.tablero_marca[row2][col2] = 0

            self.bandera1 = 0
            self.bandera2 = 0
            return False

    def muestra_tarjetas(self, row1, col1, row2, col2):
        if(self.tablero_marca[row1][col1] == 1):
            self.bandera1 = 1
        if(self.tablero_marca[row2][col2] == 1):
            self.bandera2 = 1
        self.tablero_marca[row1][col1] = 1
        self.tablero_marca[row2][col2] = 1


    def asignar_turno(self,tur):
        self.turno = tur

    def consultar_turno(self):
        return self.turno

    def juego_terminado(self):
        res = 0
        
        for row in range(0, self.size):
            for col in range(0, self.size):
                res = res + int(self.tablero_marca[row][col])
        
        return (res == self.size * self.size) 
            
    def elige_tarjetas_servidor(self):

        while True:
            random.seed(time.clock())
            row1 = random.randint(0, self.size-1)
            col1 = random.randint(0, self.size-1)
            row2 = random.randint(0, self.size-1)
            col2 = random.randint(0, self.size-1)
        
            if(self.tablero_marca[row1][col1] == 0 and self.tablero_marca[row2][col2] == 0 and row1 != row2 and col1 != col2):
                break
            
        return [row1, col1, row2, col2]
        

    def crear_tablero(self, nivel):
    #obtenemos la lista de palabras para el self.tablero        
   
        palabras = self.leer_palabras(nivel)

        for x in range(0, len(palabras)):
            palabras[x] = ''.join(palabras[x].split())[:]

        #inicializamos self.tablero
        self.tablero = [ [0 for x in range(0, self.size)] for y in range(0, self.size)]
        self.tablero_deamentis = [ [0 for x in range(0, self.size)] for y in range(0, self.size)]
        self.tablero_marca = [ [0 for x in range(0, self.size)] for y in range(0, self.size)]

        for row in range(0, self.size):
            for col in range(0, self.size):
                self.tablero[row][col] = palabras[row * self.size + col]
                self.tablero_deamentis[row][col] = "*****"


        
    def mostrar_tablero(self):
        tablero_mostrar = [ [0 for x in range(0, self.size + 1)] for y in range(0, self.size + 1)]

        tablero_mostrar[0][0] = "-"
        for x in range(0, self.size):
            tablero_mostrar[0][x + 1] = x

        for row in range(0, self.size):
            tablero_mostrar[row + 1][0] = row
            for col in range(0, self.size):
                if(self.tablero_marca[row][col] == 0):
                    tablero_mostrar[row + 1][col + 1] =  self.tablero_deamentis[row][col]
                else:
                    tablero_mostrar[row + 1][col + 1] =  self.tablero[row][col]
        return tablero_mostrar

    def tablero_string(self, tablero_mostrar):
        separador = "$$"
        tablero = []
        tablero = np.array(tablero_mostrar).ravel()
        tablero = separador.join(tablero)
        return tablero

    def marcador(self):
        res = [str(self.usuario), str(self.servidor)]
        return res

"""
memorama = Memorama()
memorama.crear_tablero("avanzado")
res = (memorama.tablero_string(memorama.mostrar_tablero()))

print(res.split("$$"))
"""

