import socket
import time

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server
buffer_size = 1024

size = 0

def crea_matriz(size, cadena):
    size = size + 1 
    tablero = [ [0 for x in range(0, size )] for y in range(0, size )]
    cadena = cadena.split("$$")
    for row in range(0, size  ):
        for col in range(0, size  ):
            tablero[row][col] = cadena[row * ( size ) + col]

    return tablero

def imprime_matriz(tablero, size):
    size = size + 1
    for x in range(0 , size):
        for y in range(0, size):
            print(tablero[x][y], end = "\t")
        print("\n")


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPClientSocket:
    TCPClientSocket.connect((HOST, PORT))
    
    TCPClientSocket.sendall(b"Hello TCP server")

    data = TCPClientSocket.recv(buffer_size)
    print(data.decode("utf-8")) 
    TCPClientSocket.sendall(b"Ok")
    data = TCPClientSocket.recv(buffer_size)
    print(data.decode("utf-8"))
    TCPClientSocket.sendall(b"Ok")
    data = TCPClientSocket.recv(buffer_size)
    print(data.decode("utf-8"))
    TCPClientSocket.sendall(b"Ok")

    while (True):

        nivel = int(input("Nivel: "))
        if(int(nivel) == 1):
            size = 4
            break
        if(int(nivel) == 2):
            size = 6
            break


    TCPClientSocket.sendall(str(nivel).encode())

    while True:
        print("tablero actual:")
        data = TCPClientSocket.recv(buffer_size).decode("utf-8")
        time.sleep(2)
        print(len(data))
        matriz = crea_matriz(size, data)
        print(imprime_matriz(matriz, size))
        TCPClientSocket.sendall(b"Ok matriz recibida")
        data = TCPClientSocket.recv(buffer_size).decode("utf-8")
        print(data)
        time.sleep(2)
        if(data == "TURNO DE USUARIO"):
            print("USUARIO")
            data = TCPClientSocket.recv(buffer_size).decode("utf-8")
            print(data)

            while(True):
                carta1 = input("")
                carta1 = carta1.split()
                if(len(carta1) == 2):
                    try:
                        c10 = int(carta1[0])
                        c11 = int(carta1[1])
                        if c10 < size and c11 < size:
                            carta1 = "$$".join(carta1)
                            TCPClientSocket.sendall(carta1.encode())
                            break
                        else:
                            print("Ingresa una coordenada correcta") 
                    except Exception as e:
                        print("Debes ingresar números")
                else:
                    print("Ingresa las coordenadas correctas")

            data = TCPClientSocket.recv(buffer_size).decode("utf-8")
            print(data)

            while(True):
                carta2 = input("")
                carta2 = carta2.split()
                if(len(carta2) == 2):
                    try:
                        c20 = int(carta2[0])
                        c21 = int(carta2[1])
                        if c20 < size and c21 < size:
                            carta2 = "$$".join(carta2)
                            TCPClientSocket.sendall(carta2.encode())
                            break
                        else:
                            print("Ingresa una coordenada correcta") 
                    except Exception as e:
                        print("Debes ingresar números")
                    
                else:
                    print("Ingresa las coordenadas correctas")

            
            data = TCPClientSocket.recv(buffer_size).decode("utf-8")
            time.sleep(2)
            matriz = crea_matriz(size, data)
            print(imprime_matriz(matriz, size))

        if(data == "TURNO DEL SERVIDOR"):
            print("SERVIDOR")
            data = TCPClientSocket.recv(buffer_size).decode("utf-8")
            time.sleep(2)
            matriz = crea_matriz(size, data)
            print(imprime_matriz(matriz, size))
            print("Jugada del servidor")
            time.sleep(2)

        if(data == "JUEGO TERMINADO"):
            resultado = TCPClientSocket.recv(buffer_size).decode("utf-8")
            resultado = resultado.split("$$")
            print("Usuario:",resultado[0], " | Servidor:", resultado[1])
            if(int(resultado[0]) > int(resultado[1])):
                print("Ha ganado el usuario")
            else:
                if(int(resultado[0]) == int(resultado[1])):
                    print("Empate")
                else:
                    print("Ha ganado el servidor")
            TCPClientSocket.close()
            break