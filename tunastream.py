import socket, io, pickle

#config
chunkSize = 8192#Change to improve preformance?


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

    def listenFile(port):
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)# create a socket object
        serverSocket.bind(('', port))# bind to the port
        serverSocket.listen(2)# queue up to 2 requests
        clientSocket,addr = serverSocket.accept()# establish a connection
        filename = clientSocket.recv(chunkSize)#The first recv is the filename
        finalFilename = filename.decode('utf-8')
        file = open(finalFilename, 'wb')#creates or overwrites new file
        while True:
            message = clientSocket.recv(chunkSize)
            if not message:
                break
            file.write(message)
        file.close()
        return finalFilename


    def sendFile(port, host, filepath):
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)# create a socket object
        clientSocket.connect((host, port))
        file = open(filepath, 'rb')#open file provided
        filenameWithoutDirectory = filepath[filepath.rfind('/')+1:]
        clientSocket.send(filenameWithoutDirectory.encode('utf-8'))#Send the filename first
        while True:
            chunk = file.read(chunkSize)#only read part of the file
            if not chunk:
                break
            clientSocket.send(chunk)

        file.close()
        clientSocket.close()
        
