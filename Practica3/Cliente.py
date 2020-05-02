import json
import socket
import logging
import time

FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] (%(threadName)-2s) %(message)s"
logging.basicConfig(level=logging.DEBUG,
                    format=FORMAT)


class Cliente:
    def __init__(self, HOST_SERVER, PORT_SERVER):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.HOST_SERVER = HOST_SERVER
        self.PORT_SERVER = PORT_SERVER
        self.BUFFER = 1024
        self.SERVER_ADD = (HOST_SERVER, PORT_SERVER)
        self.id_partida = None
        self.no_jugadores = 1

        self.socket.settimeout(5)

        #self.socket.setblocking(False)
        #self.socket.connect_ex(self.SERVER_ADD)

    def set_id_partida(self, id_partida):
        self.id_partida = id_partida

    def set_no_jugadores(self, no_jugadores):
        self.no_jugadores = no_jugadores

    def get_no_jugadores(self):
        return self.no_jugadores

    def connect_sock(self):
        msg = ""
        try:
            self.socket.connect(self.SERVER_ADD)
            logging.debug("Conexión establecida con el servidor")
            self.socket.setblocking(0)
            msg = True
        except Exception as e:
            logging.debug( "Error: %s", e)
            msg = False

        return msg

    def movimiento_cliente(self, cartas):
        msg = {
            "id_partida" : self.id_partida,
            "movimiento" : "movimiento_cliente",
            "info":
            {
                "cartas" :
                {
                    "x1" : cartas.get("x1", "ERROR"),
                    "y1" : cartas.get("y1", "ERROR"),
                    "x2" : cartas.get("x2", "ERROR"),
                    "y2" : cartas.get("y2", "ERROR")
                }
            }

        }

    def crear_partida(self, tipo, no_jugadores, nivel):
        msg = {
            "tipo_partida" : tipo,
            "movimiento" : "crear_partida",
            "no_jugador" : no_jugadores,
            "nivel" : nivel
        }

        msg = json.dumps(msg)

        self.socket.send(msg.encode())
        logging.debug("Datos enviados")

    def estado_partida(self):
        msg = {
            "movimiento": "partida"
        }

        msg = json.dumps(msg)
        self.socket.send(msg.encode())
        time.sleep(5)
        mensaje = self.socket.recv(self.BUFFER).decode("utf-8")
        estructura = json.loads(mensaje)
        logging.debug("Mensaje recibido %s", mensaje)

        return estructura["estado_partida"]

    def ingresar_partida(self, id_partida = 1):
        msg = {
            "id_partida" : id_partida,
            "movimiento" : "ingresar_partida"
        }
        msg = json.dumps(msg)
        self.socket.send(msg.encode())
        time.sleep(5)
        mensaje = self.socket.recv(self.BUFFER).decode("utf-8")
        estructura = json.loads(mensaje)
        logging.debug("Mensaje recibido %s", mensaje)

        return estructura

    def no_jugadore(self):
        msg = {
            "movimiento": "no_jugadores"
        }
        msg = json.dumps(msg)
        self.socket.send(msg.encode())
        time.sleep(5)
        mensaje = self.socket.recv(self.BUFFER).decode("utf-8")
        estructura = json.loads(mensaje)
        logging.debug("Mensaje recibido %s", mensaje)

        self.no_jugadores = estructura.get["no_jugadores"]





    # Envío de mensajes

    # Recibo de mensajes

    #

