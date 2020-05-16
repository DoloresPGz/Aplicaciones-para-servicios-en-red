from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

# Create server
with SimpleXMLRPCServer(('localhost', 8000),
                        requestHandler=RequestHandler) as server:
    server.register_introspection_functions()

    class MyFuncs:

        def muliplicacion(self, x, y):
            return x * y

        def suma(self, x, y):
            return x + y

        def resta(self, x, y):
            return x - y

        def division(self, x, y):
            if y != 0:
                return x / y
            else:
                return 0

        def potencia(self, x, y):
            return pow(x, y)

    server.register_instance(MyFuncs())

    # Run the server's main loop
    server.serve_forever()