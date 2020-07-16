import xmlrpc.client

payload = """
####################
import os, numpy as np
import requests

print(os.system("pwd"))
print(np.array(([1,2,3], [4,5,6], [7,8,9])))
print(requests.get("https://www.google.com"))
###################
"""
HOST = "localhost"
PORT = 1234

proxy = xmlrpc.client.ServerProxy("http://{}:{}/".format(HOST, PORT))

try:
	print(proxy.execute(payload, ['numpy', 'requests']))

except Exception as e:
	print("FAILURE {}".format(e))
