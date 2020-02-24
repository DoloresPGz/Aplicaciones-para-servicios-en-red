import socket
from Memorama import Memorama
import time 
import threading

#HOST = "8.40.1.192"  # The server's hostname or IP address
HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server
buffer_size = 1024

def start_conn(conn):
    print("Conexión iniciada con cliente", conn)
    while True:
        Client_conn.recv(buffer_size)

        Client_conn.sendall(b"Ingresa el nivel que desea jugar:")
        Client_conn.recv(buffer_size)
        Client_conn.sendall(b"1 Pricipiante")
        Client_conn.recv(buffer_size)
        Client_conn.sendall(b"2 Avanzado")
        Client_conn.recv(buffer_size)

        nivel = Client_conn.recv(buffer_size).decode("utf-8")

        memorama = Memorama()
        if(int(nivel) == 1):
            memorama.crear_tablero("principiante")
        if(int(nivel) == 2):
            memorama.crear_tablero("avanzado")

        while(True): #JUEGO TERMINADO

            res = (memorama.tablero_string(memorama.mostrar_tablero()))
            print("Tablero",res)
            Client_conn.send(res.encode())
            time.sleep(1)
            print(Client_conn.recv(buffer_size).decode("utf-8"))

            if(memorama.consultar_turno() == 0):
                Client_conn.sendall(b"TURNO DE USUARIO")
                time.sleep(2)
                Client_conn.sendall(b"Ingresa coordenadas de primera carta separadas por espacios")
                carta1 = Client_conn.recv(buffer_size).decode("utf-8")
                carta1 = carta1.split("$$")
                print(carta1)
                time.sleep(2)
                Client_conn.sendall(b"Ingresa coordenadas de segunda carta separadas por espacios")
                time.sleep(2)
                carta2 = Client_conn.recv(buffer_size).decode("utf-8")
                carta2 = carta2.split("$$")
                print(carta2)

                memorama.muestra_tarjetas(int(carta1[0]), int(carta1[1]), int(carta2[0]), int(carta2[1]))
                res = (memorama.tablero_string(memorama.mostrar_tablero()))
                Client_conn.sendall(res.encode())
                memorama.compara_tarjetas(int(carta1[0]), int(carta1[1]), int(carta2[0]), int(carta2[1]))

            else:
                Client_conn.sendall(b"TURNO DEL SERVIDOR")
                tarjetas = memorama.elige_tarjetas_servidor()
                print("TARJETAS SERVIDOR ", tarjetas)
                memorama.muestra_tarjetas(tarjetas[0], tarjetas[1], tarjetas[2], tarjetas[3])
                res = (memorama.tablero_string(memorama.mostrar_tablero()))
                Client_conn.sendall(res.encode())  
                memorama.compara_tarjetas(tarjetas[0], tarjetas[1], tarjetas[2], tarjetas[3])
                time.sleep(3)

            if(memorama.juego_terminado()):
                res = (memorama.tablero_string(memorama.mostrar_tablero()))
                print("Tablero",res)
                Client_conn.send(res.encode())
                time.sleep(1)
                print(Client_conn.recv(buffer_size).decode("utf-8"))

                Client_conn.sendall(b"JUEGO TERMINADO")
                time.sleep(2)
                resultado = memorama.marcador()
                resultado = "$$".join(resultado)
                Client_conn.sendall(resultado.encode())
                time.sleep(2)
                Client_conn.close()
                break


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPServerSocket:
    TCPServerSocket.bind((HOST, PORT))
    TCPServerSocket.listen()

    while True:
        Client_conn, Client_addr = TCPServerSocket.accept()
        tr = threading.Thread(target = start_conn, args = (Client_conn, ) )
        tr.start()

        
