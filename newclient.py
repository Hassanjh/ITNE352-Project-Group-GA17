import json
import socket

cs=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cs.connect(('127.0.0.1',49999))

username= input("Enter your username: ")
cs.send= username.encode('ascii')

msg=cs.recv(1024).decode('ascii')
icao= input(msg)
cs.send=icao.encode('ascii')

while True:
    print("\nSelect the option number:")
    print("1. Arrived flights")
    print("2. Delayed flights")
    print("3. All flights coming from a specific city")
    print("4. Details of a particular flight")
    print("5. Quit")

    op = input("\n Select option: ")
    cs.send(op.encode('ascii'))