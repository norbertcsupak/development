import socket
import tqdm
import os

# server IP
SERVER_HOST_IP="0.0.0.0"
SERVER_PORT=5001

#define the buffer suze
BUFFER_SIZE=4096
SEPATATOR="<SEPARATOR>"

#create socket
s = socket.socket()
s.bind((SERVER_HOST_IP, SERVER_PORT))
s.listen(5)
print(f" [*] Listening as {SERVER_HOST_IP}:{SERVER_PORT} ")

client_socket, address = s.accept()
print(f" [+] accepting connection ")
print(f" [+] {address} is connected")


received = client_socket.recv(BUFFER_SIZE).decode()
filename , filesize = received.split(SEPARATOR)

filename = os.path.basename(filename)
filesize = int(filesize)



#receiveing the file with progress bar
progress = tqdm.tqdm(range(filesize),f"Reciving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "wb") as f:
    while True:
        #read the first 1024 bytes from socket
        bytes_read = client_socket.recv(BUFFER_SIZE)
        if not bytes_read:
            # nothing to do
            # file transmittig over
            break
        f.write(bytes_read)
        # update progress bar
        progress.update(len(bytes_read))
client_socket.close()
s.close()
