# in server we'll handle all the logic of receiving the file and saving it to disk.
# also it will be responsible for sending the message to the client.

import socket
import threading
import os

class Server:
    def __init__(self, host="localhost", port=9999) -> None:
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen()
        self.clients = []
        self.files = [file for file in os.listdir("files")]
    
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
                print("LOG -> Upload operation received")
                file_name, file_size = operation.replace("<UPLOAD>", "").split("+")  # Split the message to get file name and size
                file_size = int(file_size)
                
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
                        # print("Done reading")
                        break
                    file.write(data)
                    file_size -= len(data)
                file.close()
                self.files.append(file_name)
                print("LOG -> File received") 
                self.broadcast_msg(f"LOG -> New File {file_name} was uploaded ! ")
                
            elif "<DOWNLOAD>" in operation:
                print("LOG -> Download operation received")
                file_name = operation.replace("<DOWNLOAD>", "")
                # print("File name", file_name)
                # print("FIle name: ", file_name)
                
                # send the information about the file size to the client, so it can read it correctly
                file_size = os.path.getsize(f"files/{file_name}")
                client.send(str(file_size).encode())
                # print("File size sent")

                received = client.recv(1024).decode("utf-8")
                # print(received)
                if "<READY>" in received:
                    # print("Sending File...")
                    file = open(f"files/{file_name}", "rb")
                    data = file.read()
                    client.sendall(data) 
                    file.close()
                    print("LOG -> File Sent for download")
            
            elif "<FILES>" in operation:
                print("LOG -> List Files operation received")
                files = ""
                for file in self.files:
                    files += f"{file}+"
                client.send(files.encode())
                print("LOG -> Files names sent")
                # print("Files names sent")
                
    
    def start(self):
        client_id = 0
        while True:
            client, addr = self.server.accept()
            client_id += 1
            print(f"LOG -> Connected with {str(addr)}")
            
            self.clients.append(client)
            
            # Start a new thread that will handle the client
            # This way clients can connect to the server and send files at the same time
            thread = threading.Thread(target=self.handle_client, args=(client,))
            thread.start()
            
if __name__ == "__main__":
    server = Server()
    server.start()