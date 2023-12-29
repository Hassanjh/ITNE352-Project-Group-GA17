import socket
import threading

ss = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ss.bind(("127.0.0.1",49999))

print(10*"="+" Server started "+"="*10)

ss.listen()

clients=[]
names=[]

def connection(conn,addr):
        name=conn.recv(2048).decode('ascii')
        print(f"Got a connection from {addr} with username {name}")
        clients.append(conn)
        names.append(name)
        msg = f"Hi {name}\nenter Airport code: "
        conn.send(msg.encode('ascii'))
        print(names)
        airportCode = conn.recv(2048).decode('ascii')
        print(f"Airport code from {name} is: {airportCode}")
        conn.send(f"your Airport code is {airportCode}".encode('ascii'))
        options(conn,name)

def options(conn,name):
    while True:
        op = conn.recv(2048).decode('ascii')
        print(f"{name} option is {op}")

        if op == '1':
            print("Loading arrived flights plese wait ⌛")
    
        elif op == '2':
            print("Loading delayed flights plese wait ⌛")

        elif op == '3':
            city = conn.recv(9999).decode('ascii')
            print(f"\nLoading All flights coming from {city} ⌛")

        elif op == '4':
            fnum = conn.recv(9999).decode('ascii')
            print(f"\nLoading details of flight number {fnum} plese wait ⌛")

        elif op == '5':
            print(12*"*"+" Goodbye 👋 "+"*"*12)
            break


def main():
    while True:
        conn, addr = ss.accept()
        t=threading.Thread(target=connection, args=(conn,addr))
        t.start()
        
if __name__ == '__main__':
    main()
