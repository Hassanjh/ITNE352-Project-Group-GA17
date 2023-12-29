import socket

cs = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

print(10*"="+" Client started "+"="*10)

cs.connect(("127.0.0.1",49999))

username = input("Enter a Username: ")
cs.send(username.encode('ascii'))

recvMsg = cs.recv(2024).decode('ascii')
airport_code = input(recvMsg)

cs.send(airport_code.encode('ascii'))

print(cs.recv(2048).decode('ascii'))

while True:
    print("\nSelect the number of option:")
    print("1. Arrived flights")
    print("2. Delayed flights")
    print("3. All flights coming from a specific city")
    print("4. Details of a particular flight")
    print("5. Quit")

    op = input("\nEnter option: ")
    cs.send(op.encode('ascii'))
    
    if op == '1':
        print("Loading arrived flights plese wait ⌛")
    
    elif op == '2':
        print("Loading delayed flights plese wait ⌛")

    elif op == '3':
        city = input("Enter city code: ")
        cs.send(city.encode('ascii'))
        print(f"\nLoading All flights coming from {city} ⌛")

    elif op == '4':
        fnum = input("Enter flight number: ")
        cs.send(fnum.encode('ascii'))
        print(f"\nLoading details of flight number {fnum} plese wait ⌛")

    elif op == '5':
        print(12*"*"+" Goodbye 👋 "+"*"*12)
        break

    else:
        print("Invalid Option")