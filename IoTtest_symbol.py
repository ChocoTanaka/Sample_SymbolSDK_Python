# coding= utf-8
# Tkinterで簡単なウィンドウを作成
import tkinter as tk
from tkinter import ttk
import random
import requests
import threading
import websocket
import asyncio
import json
from symbolchain.symbol.Network import Address
from tkinter import messagebox

class Node_data:
    Nodelist = ['testnet1.symbol-mikun.net', 'sym-test-03.opening-line.jp','pequod.cola-potatochips.net','2.dusanjp.com']
    Node = ''
    Address = ''
    Address_send = ''
    Message = ''
    uid = ''

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Symbol IoT")
        self.geometry("300x150")
        
        self.container = tk.Frame(self)
        self.container.pack(fill = "both",expand = True)

        self.frames = {}
        self.current_page_name = None


        self.ws = None
        # スレッドでテストを実行
        self.stop_event = threading.Event()
        self.test_thread = None
        self.stop_event.clear()
        test_thread = threading.Thread(target=self.CheckNode())
        test_thread.start()

        for F in(StartPage,PageOne,PageTwo):
            page_name = F.__name__
            frame = F(parent=self.container, controller = self)
            self.frames[page_name] = frame
            frame.grid(row = 0, column = 0, sticky="nsew")

        self.show_frame("StartPage")
        
    def show_frame(self, page_name):
        ws_instance = Websocket_class()

        if self.current_page_name == 'PageOne':
            Node_data.uid = ''
            Node_data.Message = ''
            ws_instance.waiting = False
            ws_instance.callback = False
            self.stop_event.set()  # スレッド終了フラグをセット
            if self.ws2:
                self.ws2.close()
            if self.thread and self.thread.is_alive():
                self.thread.join()
                
        frame = self.frames[page_name]
        frame.tkraise()
        self.current_page_name = page_name
        
        if page_name == "PageOne":
            Node_data.Message = ''
            self.ws2 = None
            self.thread = None
            ws_instance.waiting = True
            self.stop_event = threading.Event()
            self.stop_event.clear()
            ws_instance.start_websocket(self.ws2 ,self.thread)
        
    def get_page(self):
        return self.frames[self.current_page_name]

    def CheckNode(self):
        for node in random.sample(Node_data.Nodelist , len(Node_data.Nodelist)):
            node_test = f'https://{node}:3001/node/health'
            try:
            # URLに対してHTTP GETリクエストを送信
                response = requests.get(node_test, timeout=5)
                if response.status_code == 200:
                    Node_data.Node = node
                    print(Node_data.Node)
                    self.stop_event.set()  # スレッド終了フラグをセット
                    if self.ws:
                        self.ws.close()
                    if self.test_thread and self.test_thread.is_alive():
                        self.test_thread.join()
                    return
            except requests.RequestException as e:
                print('No node Connection')
                continue
                
class Websocket_class:
    waiting = True
    callback = False
    recieved_message = None
    ws = None
    def connect(self, ws2,thread):
        url = f'wss://{Node_data.Node}:3001/ws'  # WebSocketサーバーのURL
        ws = ws2
        self.ws = websocket.WebSocketApp(url,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         )
                # WebSocketの接続を別スレッドで実行
        thread = threading.Thread(target=self.run_websocket)
        thread.start()


    def run_websocket(self):
        self.ws.run_forever()
        
    def on_message(self,ws,message):
        self.received_message = message
        if self.callback == False:
            self.callback = True
            self.on_redirect(self.received_message)
        else:
            data = json.loads(self.received_message)
            #recipient = str(Address.from_decoded_address_hex_string(data['data']['transaction']['signature']))
            Node_data.Message = bytes.fromhex(data['data']['transaction']['message'][2:]).decode('utf-8')
            
            print(f'Message: {Node_data.Message}')
            p1 = app.get_page()
            print(p1.Getmessage())
            p1.Setmessage(Node_data.Message)
            
            
    def on_redirect(self, message):
        topic = f'confirmedAdded/{Node_data.Address}'
        data = json.loads(message)
        Node_data.uid = data['uid']
        subscribe_message = {
            "uid": Node_data.uid,
            "subscribe": topic  # ここに条件を指定
        }
        if not Node_data.uid:
            print('No Connection')
            messagebox.showerror('Error', 'No Channel Connection')
        else:
            self.ws.send(json.dumps(subscribe_message))
        
        
    def on_error(self, ws, error):
        print(f"Error: {error}")

    def start_websocket(self,ws,thread):
        self.connect(ws,thread)        
                        
class StartPage(tk.Frame):
    def __init__(self,parent,controller):
        super().__init__(parent)
        self.controller = controller
        
        label = tk.Label(self, text = "Welcome to IoT")
        label.pack(pady=15)
        if not Node_data.Node:    
            label2 = tk.Label(self, text = "No Node Connection." ,font=("Helvetica", 15),foreground = '#FF0000')
            label2.pack(pady=15)
        else:
            button1 = tk.Button(self, text = "receive", width=15, height=4, command = lambda: controller.show_frame("PageOne"))
            button1.pack(side="left", padx=10)
            button2 = tk.Button(self, text = "send", width=15, height=4, command = lambda: controller.show_frame("PageTwo"))
            button2.pack(side="right", padx=10)
        
        
        
class PageOne(tk.Frame):        
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        label = ttk.Label(self, text="This is Page One")
        label.pack(side="top", fill="x", pady=10)

        self.label2 = ttk.Label(self,text = "No Message", font=("Helvetica", 20))
        self.label2.pack(side="top", fill="x", pady=10)
        
        button = tk.Button(self, text="Back to Start",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()

    def Setmessage(self,message):
        self.label2["text"] = message
        
    def Getmessage(self):
        return self.label2["text"]

class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        label = ttk.Label(self, text="This is Page Two")
        label.pack(side="top", fill="x", pady=10)
        
        button = tk.Button(self, text="Back to Start",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()
        
if __name__ == "__main__":
    app = App()
    app.mainloop()
    
#sample
#Donate! NDUVXZD3DBJRO7FTXZ6FCWYFESNNCWBSTPUN3RI    
        
