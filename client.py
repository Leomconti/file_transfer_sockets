import socket
import os
import time

class Client:
    def __init__(self, host="localhost", port=9999, client_id=1) -> None:
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        self.client_id = client_id
    
    def upload_file(self, file_path):
        print("SENDING UPLOAD")
        self.client.send("<UPLOAD>".encode())

        file_size = os.path.getsize(file_path)

        message = f"{file_path}+{file_size}".encode()
        self.client.sendall(message)

        print(file_path)
        print(file_size)
        
        received = self.receive_message()
        if received == "<READY>":
            print("Sending File...")
            file = open(file_path, "rb")
            data = file.read()
            self.client.sendall(data) 
            file.close()
            print("File Sent")
        
    def download_file(self, file_name):
        print("SENDING DOWNLOAD")
        self.client.send("<DOWNLOAD>".encode())
        self.client.send(file_name.encode())
        
        file_size = int(self.client.recv(1024).decode("utf-8"))

        # Get the client folder (like it's downloading to its computer, used for testing locally on the same machine)
        file = open(f"clients/{self.client_id}/{file_name}", "wb")
        file_bytes = b""
        done = False
        # write the bytes into the file
        self.client.send("<READY>".encode())
        while file_size > 0:
            data = self.client.recv(1024)
            if not data:
                print("Done reading")
                break
            file.write(data)
            file_size -= len(data)
        file.close()
        print("File received") 
        
    def receive_message(self):
        message = self.client.recv(1024).decode('utf-8')
        return message
    
    # Here the client will be listening for messages from the server
    def listen(self):
        while True:
            message = self.client.recv(1024).decode("utf-8")
            print(message)
            
if __name__ == "__main__":
    client = Client()
    # client.upload_file("sc_1.png")
    client.download_file("sc_1.png")
    client.listen()