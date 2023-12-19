import socket

ss = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

ss.bind(("127.0.0.1",49999))

ss.listen(3)

client, addr = ss.accept()

username= client.recv(2024)

msg = f"Hi {username}\nenter airport code: "
client.send(msg.encode('ascii'))

recvMsg = client.recv(2024).decode('ascii')
print(f"Airport code: {recvMsg}")
