from socket import *
import tkinter,sys,threading


def tcplinks(sock,addr):
    while True:
        try:
            data = sock.recv(1024).decode()
            id = data.split(' ')[0]
            clients[id].send((addr[0]+" "+data).encode())
        except:
            sock.shutdown(2)
            clients[addr[0]] = 0

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python server.py [listen ip] [listen port]")
        sys.exit()

    clients=dict()
    
    addr = (sys.argv[2],sys.argv[3])
    tcp = socket(AF_INET,SOCK_STREAM)
    tcp.bind(addr)

    tcp.listen(100)

    while True:
        client,addr = tcp.accept()
        clients[addr[0]] = [client,1]
        t = threading.Thread(target=tcplinks,args=(client,addr))
        t.start()