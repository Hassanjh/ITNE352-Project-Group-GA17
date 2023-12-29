import socket 
import json

print(10*"="+" Client started "+"="*10)

cs=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cs.connect(('127.0.0.1',49999))

username= input("Enter your username: ")
icao=input("Enter the arr_icao code: ")
cs.send(username.encode('ascii'))
cs.send(icao.encode('ascii'))

while True:
    print("\nSelect the option:")
    print("1. Arrived flights")
    print("2. Delayed flights")
    print("3. All flights coming from a specific city")
    print("4. Details of a particular flight")
    print("5. Quit")

    option= input()
    cs.send(option.encode('ascii'))

    if option=='1':
        

