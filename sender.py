import os
import socket

# startup the client socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 9999))

# load the file and send the bytes via the network - the problem will lie with the receiver

file_name = "sc_1.png"
received_name = "received_file.png"
file_size = os.path.getsize(file_name)

message = f"{received_name}\n{file_size}".encode()
client.sendall(message)

print(received_name)
print(file_size)

file = open(file_name, "rb")  # rb  = read the bytes
data = file.read()

client.send(data)  # sendall() sends all the bytes in one go
client.send(b"<END>")  # hints the end of the file

file.close()
client.close()
