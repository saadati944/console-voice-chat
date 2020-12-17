import socket
import threading

class Server:
    def __init__(self):
        pass
    def start(self, port:int):
        self.ip = socket.gethostbyname(socket.gethostname())
        try:
            self.port = port

            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.bind((self.ip, self.port))
        except:
            return False

        self.connections = []
        self.accept_connections()

    def accept_connections(self):
        self.s.listen(100)

        #print('Running on IP: '+self.ip)
        #print('Running on port: '+str(self.port))
        
        while True:
            c, addr = self.s.accept()

            self.connections.append(c)

            threading.Thread(target=self.handle_client,args=(c,addr,)).start()
        
    def broadcast(self, sock, data):
        for client in self.connections:
            if client != self.s and client != sock:
                try:
                    client.send(data)
                except:
                    pass

    def handle_client(self,c,addr):
        while 1:
            try:
                data = c.recv(1024)
                self.broadcast(c, data)
            
            except socket.error:
                c.close()


if __name__=="__main__":
    #test
    server = Server()
    server.start(int(input("enter port for server : ")))
