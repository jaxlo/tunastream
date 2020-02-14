import socket, io, pickle

#config
chunkSize = 1024#Change to improve preformance?


class Tuna():
    def listen(port):
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)# create a socket object
        serverSocket.bind(('', port))# bind to the port to any incoming address
        serverSocket.listen(2)# queue up to 2 requests
        clientSocket,addr = serverSocket.accept()# establish a connection
        message = b''
        while True:
            chunk = clientSocket.recv(chunkSize)
            if not chunk:
                break
            message += chunk
        return pickle.loads(message)

    def send(port, host, objectToSend):
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)# create a socket object
        clientSocket.connect((host, port))
        binaryStream = io.BytesIO()#Used so part of the byte array can be split up
        binaryStream.write(pickle.dumps(objectToSend))#https://www.devdungeon.com/content/working-binary-data-python
        x = pickle.dumps(objectToSend)
        binaryStream.seek(0)# Move cursor back to the beginning of the buffer
        while True:
            chunk = binaryStream.read(chunkSize)#only get part of the bytes for the object
            if not chunk:
                break
            clientSocket.send(chunk)

        binaryStream.close()#discard the buffer in the memory
        clientSocket.close()#close the connection when the item is sent
