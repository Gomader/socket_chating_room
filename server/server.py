from socket import *
import tkinter,sys,threading


def tcplinks(sock,addr):
    while True:
        try:
            data = sock.recv(1024).decode()
            for client in clients:
                if addr[0] == client:
                    continue
                else:
                    client[0].send(client[1]+" :\n"+data.encode())
        except:
            sock.shutdown(2)
            clients[addr[0]] = 0
            logstatus(clients[addr[0]][1]+"离开了")

def logstatus(text):
    for client in clients:
        clients[client][0].send(text.encode())

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python server.py [listen ip] [listen port]")
        sys.exit()

    clients=dict()
    addr = (sys.argv[1],int(sys.argv[2]))
    tcp = socket(AF_INET,SOCK_STREAM)
    tcp.bind(addr)

    tcp.listen(100)
    while True:
        client,addr = tcp.accept()
        name = client.recv(1024).decode()
        clients[addr[0]] = [client,name,1]
        t = threading.Thread(target=tcplinks,args=(client,addr))
        t.start()
        print(addr)
        logstatus(name+"进入聊天室")