# in server we'll handle all the logic of receiving the file and saving it to disk.
# also it will be responsible for sending the message to the client.

import socket
import threading
from tqdm import tqdm
import os

class Server:
    def __init__(self, host="localhost", port=9999) -> None:
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen()
        self.clients = []
        self.files = []
    
    def broadcast_msg(self, message):
        for client in self.clients:
            client.send(message)
        
    # Function where we'll handle all the logic of receiving the file and saving it to disk.
    # Also we'll be making the file available for download for the clients
    # Broadcasting a message that a file was uploaded.
    def handle_client(self, client):
        while True:
            operation = client.recv(1024).decode("utf-8")
            # Send a message to the client that the file was uploaded, downloaded or idk
            if "<UPLOAD>" in operation:
                operation = operation.replace("<UPLOAD>", "")
            
                file_name, file_size = operation.split("+")  # Split the message to get file name and size
                file_size = int(file_size)
                print(file_name)
                print(file_size)
                
                # send the acknowledgement to the client, so it sends the file
                client.send("<READY>".encode())
                
                # create file with write bytes permission
                file = open(f"files/{file_name}", "wb")
                file_bytes = b""
                done = False
                # write the bytes into the file
                while file_size > 0:
                    data = client.recv(1024)
                    if not data:
                        print("Done reading")
                        break
                    file.write(data)
                    file_size -= len(data)
                file.close()
                print("File received") 
                
            elif "<DOWNLOAD>" in operation:
                file_name = operation.replace("<DOWNLOAD>", "")
                print("DOWNLOAD OPERATION RECEIVED")
                
                # send the information about the file size to the client, so it can read it correctly
                file_size = os.path.getsize(f"files/{file_name}")
                client.send(str(file_size).encode())

                received = client.recv(1024).decode("utf-8")
                if received == "<READY>":
                    print("Sending File...")
                    file = open(f"files/{file_name}", "rb")
                    data = file.read()
                    client.sendall(data) 
                    file.close()
                    print("File Sent")
                    
                
    
    def start(self):
        while True:
            client, addr = self.server.accept()
            print(f"Connected with {str(addr)}")
            
            self.clients.append(client)
            
            # Start a new thread that will handle the client
            # This way clients can connect to the server and send files at the same time
            thread = threading.Thread(target=self.handle_client, args=(client,))
            thread.start()
            
if __name__ == "__main__":
    server = Server()
    server.start()