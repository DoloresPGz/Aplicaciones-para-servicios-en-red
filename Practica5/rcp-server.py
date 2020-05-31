from socketserver import ThreadingMixIn
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import re
import os.path


class RPCThreading(ThreadingMixIn, SimpleXMLRPCServer):
    pass


# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


# Create server

class FileVal:
    regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    regname = re.compile("([a-zA-Z]|[0-9])+\.[a-zA-Z]+")

    def file_name(self, name):
        return False if self.regex.match(name) else True

    def file_type(self, name):
        return True if self.regname.search(name) else False


with SimpleXMLRPCServer(('localhost', 8000), requestHandler=RequestHandler) as server:
    server.register_introspection_functions()

    class MyFuncs:

        file_val = FileVal()
        static_path = "./"

        def USER_PATH(self, user):
            if not os.path.isdir(self.static_path + user):
                os.makedirs(self.static_path + user)
            return "Hello " + user

        def CREATE(self, args):
            args = args.split()
            try:
                name = "".join(args[0].split("/")[-1])
                path = "/".join(args[0].split("/")[:-1])
            except:
                msg = "Command error: CREATE [file] [data(optional)]"
                return msg
            if path:
                path += "/"
            if len(args) > 1:
                cont = " ".join(args[1:])
            else:
                cont = ""
            if os.path.isdir(self.static_path + path):
                if not os.path.isfile(self.static_path + path + name):
                    if self.file_val.file_name(name):
                        if self.file_val.file_type(name):
                            file = open(self.static_path + path + name, "w+")
                            file.write(cont)
                            file.close()
                            msg = name + " file created"
                        else:
                            msg = "Must specify the type file"
                    else:
                        msg = "The name " + name + " is not valid"
                else:
                    msg = "The file " + name + " already exists"
            else:
                msg = "The path " + path + " does not exit, you must create it first"

            return msg

        def READ(self, args):
            args = args.split()
            try:
                name = "".join(args[0].split("/")[-1])
                path = "/".join(args[0].split("/")[:-1])
            except:
                msg = "Command error: READ [file]"
                return msg
            if path:
                path += "/"
            if os.path.isdir(self.static_path + path):
                if os.path.isfile(self.static_path + path + name):
                    file = open(self.static_path + path + name, "r")
                    data = file.read()
                    file.close()
                    msg = data
                else:
                    msg = "The file " + name + " does not exists"
            else:
                msg = "The path " + path + " does not exit"

            return msg

        def WRITE(self, args):
            args = args.split()
            try:
                name = "".join(args[0].split("/")[-1])
                data = " ".join(args[1:])
                path = "/".join(args[0].split("/")[:-1])
            except:
                msg = "Command error: WRITE [file] [data]"
                return msg
            if path:
                path += "/"
            if os.path.isdir(self.static_path + path):
                if os.path.isfile(self.static_path + path + name):
                    print(self.READ(self.static_path + path + name))
                    file = open(self.static_path + path + name, "a")
                    file.write(data)
                    file.close()
                    msg = "El archivo " + name + " fue reescrito"
                else:
                    msg = "The file " + name + " does not exists"
            else:
                msg = "The path " + path + " does not exit"

            return msg

        def RENAME(self, args):
            args = args.split()
            try:
                old_name = "".join(args[0].split("/")[-1])
                new_name = "".join(args[1].split("/")[-1])
                path = "/".join(args[0].split("/")[:-1])
            except:
                msg = "Command error: RENAME [old_name] [new_name]"
                return msg
            if path:
                path += "/"
            if os.path.isdir(self.static_path + path):
                if os.path.isfile(self.static_path + path + old_name):
                    if self.file_val.file_name(new_name):
                        if self.file_val.file_type(new_name):
                            os.rename(self.static_path + path + old_name, self.static_path + path + new_name)
                            msg = "The file " + old_name + " is now named as " + new_name
                        else:
                            msg = "Must specify the type file"
                    else:
                        msg = "The name " + new_name + " is not valid"
                else:
                    msg = "The file " + old_name + " does not exists"
            else:
                msg = "The path " + path + " does not exit"
            return msg

        def REMOVE(self, args):
            args = args.split()
            try:
                name = "".join(args[0].split("/")[-1])
                path = "/".join(args[0].split("/")[:-1])
            except:
                msg = "Command error: REMOVE [path]"
                return msg
            if path:
                path += "/"
            if os.path.isdir(self.static_path + path):
                if os.path.isfile(self.static_path + path + name):

                    os.remove(self.static_path + path + name)
                    msg = "The file " + name + " has been removed"

                else:
                    msg = "The file " + self.static_path + path + name + " does not exists"
            else:
                msg = "The path " + path + " does not exit"
            return msg

        def MKDIR(self, args):
            args = args.split()
            try:
                path = args[0]
            except:
                msg = "Command error: MKDIR [path]"
                return msg

            if not os.path.isdir(self.static_path + path):
                os.makedirs(self.static_path + path)
                msg = "The path " + path + " has been created"
            else:
                msg = "The path " + path + " already exists"

            return msg

        def RMDIR(self, args):
            args = args.split()
            try:
                path = args[0]
            except:
                msg = "Command error: MKDIR [path]"
                return msg

            if os.path.isdir(self.static_path + path):
                try:
                    os.rmdir(self.static_path + path)
                    msg = "The path " + path + " has been removed"
                except:
                    msg = "something went wrong"
            else:
                msg = "The path " + path + " does not exists"

            return msg

        def READDIR(self, path):

            startpath = self.static_path + path

            return os.listdir(startpath)


    server.register_instance(MyFuncs())
    # Run the server's main loop
    server.serve_forever()
