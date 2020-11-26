from socket import *
import tkinter,sys,threading

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python server.py [listen ip] [listen port]")
        sys.exit()

    clients=dict()
    