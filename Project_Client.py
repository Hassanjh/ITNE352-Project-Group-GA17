import socket

cs = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

cs.connect(("127.0.0.1",49999))

username = input("Enter a Username: ")

cs.send(username.encode('ascii'))

recvMsg = cs.recv(2024).decode('ascii')
airport_code = input(recvMsg)

cs.send(airport_code.encode('ascii'))

while True:
    print("\nSelect the number of option:")
    print("1. Arrived flights")
    print("2. Delayed flights")
    print("3. All flights coming from a specific city")
    print("4. Details of a particular flight")
    print("5. Quit")

    op = input("\nEnter option: ")
    if op == '5':
        print(12*"*"+" Goodbye "+"*"*12)
        cs.send("quit".encode('ascii'))
        break
    elif op in ['1', '2', '3', '4']:
        cs.send(op.encode('ascii'))
    else:
        print("Invalid Option")
