import socket
import os
from tqdm import tqdm

class Client:
    def __init__(self, host="localhost", port=9999, client_id=1) -> None:
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        self.client_id = client_id
    
    def upload_file(self, file_path):
        print("SENDING UPLOAD")
        try:
            file_size = os.path.getsize(file_path)
        except FileNotFoundError:
            print("ERROR -> File not found")
            return
        self.client.send(f"<UPLOAD>{file_path}+{file_size}".encode())

        print(file_path)
        print(file_size)
        
        received = self.receive_message()
        if received == "<READY>":
            file = open(file_path, "rb")
            data = file.read()
            self.client.sendall(data) 
            file.close()
        
    def download_file(self, file_name):
        # print("LOG -> SENDING DOWNLOAD")
        self.client.send("<DOWNLOAD>".encode())
        self.client.send(file_name.encode())
        
        file_size = int(self.client.recv(1024).decode("utf-8"))
        # print("File size received")

        # write the bytes into the file
        self.client.send("<READY>".encode())
        # print("Sent acknowledgement")
        file = open(f"clients/{self.client_id}/{file_name}", "wb")
        file_bytes = b""
        done = False
        progress_bar = tqdm(range(file_size), f"Downloading {file_name}", unit="B", unit_scale=True, unit_divisor=1024)
        while file_size > 0:
            data = self.client.recv(1024)
            if not data:
                break
            file.write(data)
            progress_bar.update(len(data))
            file_size -= len(data)
        file.close()
        
    def receive_message(self):
        message = self.client.recv(1024).decode('utf-8')
        return message
    
    # Here the client will be listening for messages from the server
    def listen(self):
        while True:
            message = self.client.recv(1024).decode("utf-8")
            print(message)
    
    def get_files_list(self):
        self.client.send("<FILES>".encode())
        files = self.client.recv(1024).decode("utf-8").rstrip("+").split("+")
        return files
        

def main():
    client = Client()
    running = True
    while running:
        print("### CLIENT MENU ###")
        print("1. Upload File")
        print("2. Download File")
        print("3. Exit")
        choice = int(input("Select Operation: "))
        print("\n" for _ in range(5)())
        match choice:
            case 1:
                # Upload file
                print("### UPLOAD FILE ###")
                file_path = str(input("Enter the file path:"))
                client.upload_file(file_path)
                print("INFO -> File uploaded")
            case 2:
                # Download file
                print("### DOWNLOAD FILE ###")
                print("Available files: ")
                files = client.get_files_list()
                for i, file in enumerate(files):
                    print(f"{i}. {file}")
                file_index = int(input("Enter the file number:"))
                file_name = files[file_index]
                client.download_file(file_name)
                print("INFO -> File downloaded")
            case 3:
                # Exit
                print("INFO -> Exiting...")
                client.client.close()
                running = False
                break
        print("LOG -> Operation Completed")
        print("\n" for _ in range(5)())              
            
if __name__ == "__main__":
    main()
