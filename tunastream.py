import socket


class Tuna():
    def listen(port):
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # get local machine name
        host = ''#socket.gethostname()

        # bind to the port
        serversocket.bind((host, port))

        serversocket.listen(2)# queue up to 2 requests

        # establish a connection
        clientsocket,addr = serversocket.accept()
        file = open('newFile.png', 'wb')
        while True:
            message = clientsocket.recv(1000000)
            if not message:
                break
            file.write(message)
        #clientsocket.close()
        file.close()

        return message


    def send(port, host, filepath):

        # create a socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # connection to hostname on the port
        s.connect((host, port))

        file = open(filepath, 'rb')
        while True:
            chunk = file.read(1000000)#1 mb
            if not chunk:
                break
            s.send(chunk)

        file.close()
        s.close()
