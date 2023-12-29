import json 
import threading 
import socket
from pip._vendor import requests

ss=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ss.bind(('127.0.0.1',49999))