# (c) Intzaar
# File Transfer using python3
# file_server 0.2
# ---------------------------------
host = ''
port = 9999
buffer = 64
file = 'file-name-or-path'
# ---------------------------------

import socket, os
try:
    from tqdm import tqdm
except:
    os.system('pip3 install tqdm')
    from tqdm import tqdm

def make_connection(host,port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host,port))
    s.listen(1)
    print('Waiting for connection...')
    c,addr = s.accept()
    print('Connected with',addr[0], addr[1])
    c.send(b'Connection established.')
    return c

def send_file(c, file, buffer):
    sep='<SEP>'
    basename = os.path.basename(file)
    filesize = os.path.getsize(file)
    info = basename+sep+str(buffer)+sep+str(filesize)
    c.send(info.encode())
    print('Name :',basename,'\nSize :',filesize,'bytes')
    with open(file, 'rb') as f:
        for i in tqdm(range((filesize//buffer)+1)):
            line = f.read(buffer)
            c.send(line)
    ack = c.recv(4).decode()
    if ack == 'ack':
        print('File Transfered.\n')
    c.close()

if __name__ == '__main__':
    c = make_connection(host,port)
    send_file(c,file,buffer)