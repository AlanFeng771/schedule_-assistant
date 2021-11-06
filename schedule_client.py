import socket

HOST = '13.67.33.248'
PORT = 8080

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
allow_input = False
while True:
    if allow_input:
        msg = input('>')
        client.sendall(msg.encode())
            
    serverMessage = str(client.recv(1024), encoding='utf-8')
    message = serverMessage.split(' ')
    if message[0] == 'exit':
        allow_input = False
        break
    
    if message[0] == 'hello':
        allow_input = False
        print(f'Server : {serverMessage}')
    
    if message[0] == 'schedule':
        allow_input = False
        print(f'Server : {serverMessage}')

    if message[0] == 'show':
        allow_input = False
        results = client.recv(1024).decode('utf-8')
        print(results)
        print(f'Server : {serverMessage}')
        allow_input = True

    if message[0] == 'allow_input':
        allow_input = True


    
client.close()
