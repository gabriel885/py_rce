from socketserver import ThreadingMixIn
from xmlrpc.server import SimpleXMLRPCServer
from virenv import virtual_environment_decorator


class RemoteCodeExecutionThreadedServer(ThreadingMixIn, SimpleXMLRPCServer):
	VIRTUAL_ENVIRONMENTS_PATH = "./envs"  # where to create virtual environments
	
	def __init__(self, host, port, *args, **kwargs):
		SimpleXMLRPCServer.__init__(self, (host, port), *args, **kwargs)
		print("Starting v1 server on {}:{}".format(host, port))
	
	def run(self):
		""" run server"""
		self.serve_forever()
	

@virtual_environment_decorator(base=RemoteCodeExecutionThreadedServer.VIRTUAL_ENVIRONMENTS_PATH)
def execute(code="", requirements=[]):
	""" execute code with requirements inside virtual environment """
	pass


if __name__ == '__main__':
	HOST = "localhost"
	PORT = 1234
	
	server = RemoteCodeExecutionThreadedServer(HOST, PORT)
	server.register_function(execute, "execute")
	server.run()
	pass
