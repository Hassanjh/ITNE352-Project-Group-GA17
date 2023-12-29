import socket
import threading
import json
from pip._vendor import requests

print (10*"-","The server has started",10*"-")

arriicao= input("Enter arrival airport code: ")
ss= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ss.bind(("127.0.0.1",49999))

ss.listen(3)
