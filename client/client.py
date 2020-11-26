from socket import *
import tkinter as tk
import tkinter.filedialog,sys,threading,time,json
    

class chatting:
    def __init__(self,ip='127.0.0.1',port=80,name="NONE"):
        self.name = name
        self.ip = ip
        self.port = port
        self.root = tk.Tk()
        self.root.title('chating...')

        self.frames = [tk.Frame(),tk.Frame(),tk.Frame(),tk.Frame(),tk.Frame(),tk.Frame()]

        self.members = tk.Listbox(self.frames[4])


        self.chatTextScrollBar = tk.Scrollbar(self.frames[0])
        self.chatTextScrollBar.pack(side=tk.RIGHT,fill=tk.Y)

        self.chatText = tk.Listbox(self.frames[0],width=70,height=18)
        self.chatText['yscrollcommand'] = self.chatTextScrollBar.set
        self.chatText.pack(expand=1,fill=tk.BOTH)
        self.chatTextScrollBar['command'] = self.chatText.yview()
        self.frames[0].pack(expand=1,fill=tk.BOTH)

        label = tk.Label(self.frames[1],height=2)
        label.pack(fill=tk.BOTH)
        self.frames[1].pack(expand=1,fill=tk.BOTH)

        self.inputText = tk.Text(self.frames[2],width=70,height=8)
        self.inputText.pack(expand=1,fill=tk.BOTH)
        self.frames[2].pack(expand=1,fill=tk.BOTH)

        self.sendButton = tk.Button(self.frames[3],text='发 送',width=10,command=self.sendMessage)
        self.sendButton.pack(expand=1,side=tk.BOTTOM and tk.RIGHT,padx=25,pady=5)

        self.sendfile = tk.Button(self.frames[3],text='文 件',width=10,command=self.sendfile)
        self.sendfile.pack(expand=1,side=tk.RIGHT,padx=25,pady=5)

        self.frames[3].pack(expand=1,fill=tk.BOTH)

    def recveiveMessage(self):
        self.tcp = socket(AF_INET,SOCK_STREAM)
        self.tcp.connect((self.ip,self.port))
        self.tcp.send(self.name.encode())
        while True:
            data = self.tcp.recv(1024).decode()
            if data == "file":
                filename = self.tcp.recv(1024).decode()
                f = open(filename,'w')
                f.close()
                while True:
                    data = self.tcp.recv(1024).decode()
                    if data == "finished":
                        break
                    f = open(filename,'ab')
                    f.write(data)
                    f.close()
                os.system(filename)
            else:
                now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                self.chatText.insert(tk.END,now)
                self.chatText.insert(tk.END,data)
    def sendMessage(self):
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        message = self.inputText.get('1.0',tk.END)
        self.chatText.insert(tk.END,now)
        self.chatText.insert(tk.END,message)
        self.tcp.send(self.name+":"+message.encode())
    
    def sendfile(self):
        filename = tk.filedialog.askopenfilename(title="选择文件")
        tcp.send("file".encode())
        time.sleep(0.2)
        tcp.send(filename.split('/')[-1].encode())
        f = open(filename,'rb')
        for data in f:
            tcp.send(data)
        time.sleep(0.2)
        tcp.send("finished".encode())
        f.close()
    def insertTothread(self):
        threading.Thread(target=self.recveiveMessage)
        

if __name__ == "__main__":
    name = input("请输入你的名字：")
    try:
        ch = chatting(sys.argv[1],int(sys.argv[2]),name)
    except:
        ch = chatting
    ch.insertTothread()
    ch.root.mainloop()