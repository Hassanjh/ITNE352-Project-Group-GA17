import socket

cs = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

print(10*"="+" Client started "+"="*10)
cs.connect(("127.0.0.1",49999))

username = input("Enter a Username: ")
# Sending the username to the server
cs.send(username.encode('ascii'))

# Displaying options and asking the user to enter an option
while True:
    print("\nSelect the number of option:")
    print("1. Arrived flights")
    print("2. Delayed flights")
    print("3. All flights coming from a specific city")
    print("4. Details of a particular flight")
    print("5. Quit")

    op = input("\nEnter option: ")
    #Sending the option to the server
    cs.send(op.encode('ascii'))

    if op == '1':
        print("Loading arrived flights please wait ⌛ ")
        arrived = cs.recv(20400).decode('ascii')
        print(arrived)
    elif op == '2':
        print("Loading delayed flights please wait ⌛ ")
        delayed = cs.recv(20400).decode('ascii')
        print(delayed)
    elif op == '3':
        city = input("Enter Depature IATA code: ")
        cs.send(city.encode('ascii'))
        print(f"\nLoading All flights coming from {city} ⌛ ")
        city_airport = cs.recv(20400).decode('ascii')
        print(city_airport)
    elif op == '4':
        fnum = input("Enter flight IATA code: ")
        cs.send(fnum.encode('ascii'))
        print(f"\nLoading details of flight number {fnum} plese wait ⌛ ")
        specific = cs.recv(20400).decode('ascii')
        print(specific)
    elif op == '5':
        print(12*"*"+" Goodbye 👋 "+"*"*12)
        break
    else:
        print("Invalid Option")