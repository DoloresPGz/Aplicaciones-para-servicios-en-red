import xmlrpc.client
import datetime
s = xmlrpc.client.ServerProxy('http://localhost:8000')

opc = "s"

dic = {
    1 : s.suma,
    2 : s.resta,
    3 : s.multiplicacion,
    4 : s.division,
    5 : s.potencia
}

while opc == "S" or opc == "s":
    print("Selecciona un número para la operación a realizar")
    print("1 Suma")
    print("2 Resta")
    print("3 Multiplicación")
    print("4 Divisón")
    print("5 Potencia")

    try:
        res = int(input("Número: "))
        no1 = int(input("Primer número: "))
        no2 = int(input("Segundo número: "))
    except:
        print("debe ingresar números")
        break

    fun = dic.get(res, "No existe esa opción")
    try:
        print("El resultado es:",fun(no1, no2))
    except:
        print(fun)
    opc = input("¿quieres realizar otra operación? s/n ")

# Print list of available methods
print(s.system.listMethods())