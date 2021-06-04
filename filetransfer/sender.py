import socket
import tqdm
import os
import argparse

parser = argparse.ArgumentParser(description='file receiver ')
parser.add_argument('--port',type=int, help='send to  server port for incoming calls ',required=True)
parser.add_argument('--receiver',type=str, help="receiver IP", required=True)
parser.add_argument('--file',type=str, help="file to transfer", required=True)
args = parser.parse_args()



SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096 # send 4096 bytes each time step


host = args.receiver
port = args.port
filename = args.file
filesize = os.path.getsize(filename)

s=socket.socket()

print(f" [+] connecting to {host}:{port}")
s.connect((host, port))
print(f" [+] Connected")

s.send(f"{filename}{SEPARATOR}{filesize}".encode())

progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "rb") as f:
    while True:
        # read the bytes from the file
        bytes_read = f.read(BUFFER_SIZE)
        if not bytes_read:
            # file transmitting is done
            break
        # we use sendall to assure transimission in
        # busy networks
        s.sendall(bytes_read)
        # update the progress bar
        progress.update(len(bytes_read))
# close the socket
s.close()
