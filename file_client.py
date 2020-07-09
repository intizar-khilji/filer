# (c) Intzaar
# File Transfer using python3
# file_client 0.2
# ---------------------------------
host = 'localhost'
port = 9999
# ---------------------------------

import socket, os
try:
    from tqdm import tqdm
except:
    os.system('pip3 install tqdm')
    from tqdm import tqdm

def make_connection(host,port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    print(s.recv(32).decode())
    return s

def recv_file(s,path=''):
    sep='<SEP>'
    info = s.recv(1024).decode()
    info  = info.split(sep)
    file = path+info[0]
    buffer = int(info[1])
    filesize = int(info[2])
    re = b''
    print('Name :',os.path.basename(file),'\nSize :',filesize,'Bytes')
    with open(file, 'wb') as f:
        for i in tqdm(range((filesize//buffer)+1)):
            line = s.recv(buffer)
            f.write(line)
    filesize2 = os.path.getsize(file)
    if filesize == filesize2:
        s.send(b'ack')
        print('Transmission Successfully Completed.\n')
    s.close()

if __name__ == '__main__':
    s = make_connection(host,port)
    recv_file(s,'D:\\Projects\\s\\')