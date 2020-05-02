import socket
import threading
import json
import Partida
import logging
from functools import partial

FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] (%(threadName)-2s) %(message)s"
logging.basicConfig(level=logging.DEBUG,
                    format=FORMAT)

class Servidor:
    def __init__(self, HOST = "127.0.0.1", PORT = 54321):
        self.HOST = HOST
        self.PORT = PORT
        self.BUFFER = 1024
        self.socket = None
        self.partidas_list = list()
        self.estado_partida = False
        self.sockets_list = list()
        self.SOCKET_ADDR = (HOST, PORT)

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.SOCKET_ADDR)
        self.socket.listen()

        self.menu = {
            "ingresar_partida" : self.ingresar_partida,
            "crear_partida" : self.crear_partida,
            "movimiento_cliente" : self.movimiento_cliente,
            "asignar_turno" : self.asignar_turno,
            "enviar_resultado" : self.enviar_resultado,
            "nuevo_jugador" : self.nuevo_jugador,
            "partida" : self.partida,
            "no_jugadores" : self.no_jugadores

        }

    def functions(self, name):
        func = self.menu.get(name, lambda: "nothing")
        return func()


    def nueva_conexion(self):
        try:
            while True:
                logging.debug("Esperando nueva conexión...")
                client_conn, client_addr = self.socket.accept()
                logging.debug("Nueva conexión a %s", client_addr)
                self.sockets_list.append(client_conn)
                thread_client = threading.Thread(target = self.recibir_datos, args = [client_conn, client_conn])
                thread_client.start()
        except Exception as e:
            logging.debug("Error:  %s", e)

    def partida(self, client_conn, estructura):
        msg = {
            "estado_partida" : self.estado_partida,
            "id_partida" : 1,
        }
        msg = json.dumps(msg)
        client_conn.send(msg.encode())
        logging.debug("estado partida")


    def recibir_datos(self, client_conn, client_addr):
        #try:
        logging.debug("Recibiendo datos")
        while True:
            logging.debug("Recibiendo datos de %s", client_addr)
            mensaje = client_conn.recv(self.BUFFER).decode("utf-8")
            if not mensaje:
                logging.debug("Se perdió la conexión de este cliente")
                self.sockets_list.remove(client_conn)
                break
            estructura = json.loads(mensaje)
            logging.debug("Mensaje recibido %s", mensaje)
            func = self.menu.get(estructura["movimiento"], None)
            if func:
                func(client_conn, estructura)
            else:
                logging.debug("Pusiste una función que no existe :B")
        #except Exception as e:
         #   logging.debug("Error: %s", e)

    def crear_partida(self, conn, estructura):
        logging.debug("Creando partida")
        self.estado_partida = True
        tipo_partida = estructura["tipo_partida"]
        no_jugadores = estructura["no_jugador"]
        nivel = estructura["nivel"]
        jugador = conn
        partida = Partida.Partida(jugador, tipo_partida, nivel, no_jugadores)
        logging.debug("Objeto creado")
        self.partidas_list.append(partida)
        partida.set_id_partida(len(self.partidas_list))
        mensaje = {
            "id_partida" : partida.get_id_partida()
        }
        logging.debug("Partida creada: %s", mensaje)
        partida.empezar_partida(conn)


    def ingresar_partida(self, conn, estructura):
        #no_partida = estructura["no_partida"]
        jugador = conn
        self.partidas_list[0].empezar_partida(jugador)
        msg = {"tipo": self.partidas_list[0].get_tipo_partida(), "no_jugador": self.partidas_list[0].get_no_jugadores(), "nivel": self.partidas_list[0].get_nivel()}
        msg = json.dumps(msg)
        conn.send(msg.encode())

    def no_jugadores(self, conn, estructura):
        msg = {
            "no_jugadores" : len(self.sockets_list)
        }
        msg = json.dumps(msg)
        conn.send(msg.encode())

    def movimiento_cliente(self, conn, estructura):

        logging.debug("Enviando movimiento al tablero")

    def asignar_turno(self, conn, estructura):
        logging.debug("Asignando turno a cliente")

    def enviar_resultado(selfs, conn, estructura):
        logging.debug("Enviando reusultado a clientes")

    def cerrar_conexion(self, conn, estructura):
        logging.debug("Cerrando conexión con cliente")

    def nuevo_jugador(self, conn, estructura):
        logging.debug("Nuevo jugador a la partida")


servidor = Servidor()

servidor.nueva_conexion()

