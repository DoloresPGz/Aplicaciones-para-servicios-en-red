import xmlrpc.client
import os.path


s = xmlrpc.client.ServerProxy('http://localhost:8000')
print(s.system.listMethods())


dic = {
    "CREATE" : s.CREATE,
    "READ" : s.READ,
    "WRITE" : s.WRITE,
    "RENAME" : s.RENAME,
    "REMOVE" : s.REMOVE,
    "MKDIR" : s.MKDIR,
    "RMDIR" : s.RMDIR,
    "READDIR" : s.READDIR

}

user = input("User name: ")
user = "".join(user)
print(s.USER_PATH(user))

while True:
    comand = input().split()
    fun = dic.get(comand[0], None)
    if fun:
        body = str(user + "/"+" ".join(comand[1:]))
        print(fun(body))
    else:
        print("Command not recognised")

