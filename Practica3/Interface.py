import tkinter as tk
import Cliente
import logging

FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] (%(threadName)-2s) %(message)s"
logging.basicConfig(level=logging.DEBUG,
                    format=FORMAT)

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.frame = None
        self.cambiar_frame(MainFrame)
        self.cliente = None

    def cambiar_frame(self, clase_frame, arg = None):

        nuevo_frame = clase_frame(self, arg)

        if self.frame is not None:
            self.frame.destroy()
        self.frame = nuevo_frame
        self.frame.pack()

    def set_cliente(self, cliente):
        self.cliente = cliente


class MainFrame(tk.Frame):
    def __init__(self, parent, arg):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.lbl_info = tk.Label(self, text = "Ingrese la información del servidor")
        self.lbl_host = tk.Label(self, text = "Host")
        self.lbl_puerto = tk.Label(self, text = "Puerto")
        self.en_host = tk.Entry(self, width = 40)
        self.en_host.insert("end", '127.0.0.1')
        self.en_puerto = tk.Entry(self, width = 40)
        self.en_puerto.insert("end", "54321")
        self.btn_entrar = tk.Button(self, text = "Entrar", command = lambda : self.get_connection())

        self.lbl_info.grid(row = 0, column = 0, columnspan = 2)
        self.lbl_host.grid(row = 1, column = 0)
        self.en_host.grid(row = 1, column = 1)
        self.lbl_puerto.grid(row = 2, column = 0)
        self.en_puerto.grid(row = 2, column = 1)
        self.btn_entrar.grid(row = 3, column = 0, columnspan = 2)

    def get_connection(self):
        host = self.en_host.get()
        try:
            port = int(self.en_puerto.get())
        except:
            port = 54321
        self.parent.set_cliente(Cliente.Cliente(host, port))
        if self.parent.cliente.connect_sock():
            if self.parent.cliente.estado_partida():
                arg = self.parent.cliente.ingresar_partida()
                self.parent.cambiar_frame(Espera, arg)
            else:
                self.parent.cambiar_frame(Jugador)


class Jugador(tk.Frame):
    def __init__(self, parent, arg):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.lbl_info = tk.Label(self, text = "Selecciona el tipo de juego")
        self.btn_servidor = tk.Button(self, text = "Jugar con el servidor", command = lambda: self.parent.cambiar_frame(Partida, "servidor"))
        self.btn_usuario = tk.Button(self, text = "Jugar con multiusuarios", command = lambda: self.parent.cambiar_frame(Partida, "multiusuario"))

        self.lbl_info.grid(row = 0, column = 0)
        self.btn_servidor.grid(row = 1, column = 0)
        self.btn_usuario.grid(row = 2, column = 0)




class Partida(tk.Frame):
    def __init__(self, parent, tipo):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.tipo = tipo
        if self.tipo == "servidor":
            self.state = "disabled"
        else:
            self.state = "readonly"

        self.option = tk.StringVar()
        self.lbl_tipo = tk.Label(self, text = "Tipo de juego: " + self.tipo)
        self.lbl_info = tk.Label(self, text = "Configura la partida nueva")
        self.lbl_nivel = tk.Label(self, text = "Niviel")
        self.lbl_jugadores = tk.Label(self, text = "Número de jugadores")
        self.rb_avanzado = tk.Radiobutton(self, text = "Avanzado", value = "avanzado", variable = self.option)
        self.rb_prin = tk.Radiobutton(self, text = "Pricipiante", value = "principiante", variable = self.option)
        self.btn_jugar = tk.Button(self, text = "Jugar", command = lambda: self.get_values())
        self.sb_jugadores = tk.Spinbox(self, from_= 2, to = 5, width = 5, state = self.state)

        self.rb_prin.select()

        self.lbl_tipo.grid(row = 0, column = 0, columnspan = 2)
        self.lbl_info.grid(row = 1, column = 0, columnspan = 3)
        self.lbl_nivel.grid(row = 2, column = 0, columnspan = 2)
        self.lbl_jugadores.grid(row = 2, column = 2)
        self.rb_prin.grid(row = 3, column = 0)
        self.rb_avanzado.grid(row = 3, column = 1)
        self.sb_jugadores.grid(row = 3, column = 2)
        self.btn_jugar.grid(row = 4, column = 0, columnspan = 3)

    def get_values(self):
        arg = {"tipo" : self.tipo,"no_jugador": self.sb_jugadores.get(), "nivel": self.option.get()}
        self.parent.cliente.crear_partida(arg["tipo"], arg["no_jugador"], arg["nivel"])
        if arg["tipo"] == "servidor":
            self.parent.cambiar_frame(Tablero, arg)
        if arg["tipo"] == "multiusuario":
            self.parent.cambiar_frame(Espera, arg)




class Espera(tk.Frame):
    def __init__(self, parent, arg):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.jugadores = arg["no_jugador"]
        self.arg = arg

        self.lbl_espera = tk.Label(self, text = "Espera a que se llene la partida")
        self.lbl_no_jugador = tk.Label(self, text = "")

        self.lbl_espera.grid(row = 0, column = 0)
        self.lbl_no_jugador.grid(row = 1, column = 0)

        self.counter_label(self.lbl_no_jugador)


    def counter_label(self, label):
        def count():
            self.parent.cliente.no_jugadore()
            #self.parent.cambiar_frame(Espera, arg)
            no_jugador = self.parent.cliente.get_no_jugadores()
            label.config(text=str(no_jugador) + "/" + str(self.jugadores))
            if int(self.jugadores) == int(no_jugador):
                self.parent.cambiar_frame(Tablero, self.arg)
            label.after(1000, count)

        count()


class Tablero(tk.Frame):
    def __init__(self, parent, arg):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.jugadores = arg["no_jugador"]
        self.nivel = arg["nivel"]
        self.cartas = []
        self.cartas_selec = 0
        self.no_cartas = 0
        self.contador = 0
        if self.nivel == "principiante":
            self.no_cartas = 4
        else:
            self.no_cartas = 6

        self.lbl_tiempo = tk.Label(self, text = "Tiempo:")
        self.lbl_contador = tk.Label(self, text = "")
        self.lbl_info = tk.Label(self, text = "")

        self.cartas = [[0 for x in range(self.no_cartas)] for x in range(self.no_cartas)]
        for x in range(self.no_cartas):
            for y in range(self.no_cartas):
                self.cartas[x][y] = tk.Button(self, text = "", width =10, height = 5, highlightthickness=10, bg = "blue", bd = 10, command=lambda x=x, y=y: self.change(x, y))
                self.cartas[x][y].grid(column=x, row=y)
        self.lbl_info.grid(row = self.no_cartas, column = 0, columnspan = self.no_cartas)
        self.lbl_tiempo.grid(row = self.no_cartas + 1, column = 0, stick = "e")
        self.lbl_contador.grid(row = self.no_cartas + 1, column = 1, stick = "w")
        self.counter_label(self.lbl_contador)

    def change(self, x, y):
        if self.cartas_selec != 2:
            self.cartas_selec = self.cartas_selec + 1
            self.cartas[x][y].config(bg="white", borderwidth=4, text = "palabra")
            if self.cartas_selec == 2:
                self.bloquea()

    def bloquea(self):
        for x in range(self.no_cartas):
            for y in range(self.no_cartas):
                self.cartas[x][y].config(state = "disable")


    def counter_label(self,label):
        def count():
            self.contador
            self.contador += 1
            label.config(text=str(self.contador))
            label.after(1000, count)
        count()

app = App()
app.mainloop()