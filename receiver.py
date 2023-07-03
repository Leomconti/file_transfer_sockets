import socket
import tqdm

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 9999))
server.listen()

client, addr = server.accept()

combined_message = client.recv(1024).decode('utf-8')  # Receive the combined message
file_name, file_size = combined_message.split("\n")  # Split the message to get file name and size

print(file_name)
print(file_size)

file = open(file_name, "wb")
file_bytes = b""

done = False

# progress bar
progress = tqdm.tqdm(unit="B", unit_scale=True, unit_divisor=1000, 
                     total=int(file_size))

while not done:
    data = client.recv(1024)
    if file_bytes[-5:] == b"<END>":
        done = True
    else:
        file_bytes += data
        
    progress.update(len(data))  # update the progress bar

file.write(file_bytes)

file.close()
client.close()
server.close()
