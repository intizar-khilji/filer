# (c) Intzaar
# File Transfer using python3
# file_client 0.2
# ---------------------------------
host = 'localhost'
port = 9999
# ---------------------------------

import socket, os, sys,time
try:
    from tqdm import tqdm
except:
    os.system('pip3 install tqdm')
    from tqdm import tqdm

args = sys.argv
if len(args)>1:
    host = args[1]
else:
    print('args[1] - Host IP Address\nDefault IP Address - localhost\n\n')

def make_connection(host,port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    i,n = 0,5
    while i<n:
        try:
            s.connect((host, port))
            break
        except:
            print(f'[-] Retrying({i+1})...')
            time.sleep(0.5)
            i+=1
            if i == n:
                print('[-] Not connected.')
                sys.exit()
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
    print('Received File Size :',filesize2,'Bytes')
    if filesize == filesize2:
        s.send(b'ack')
        print('[+] Transmission Successfully Completed.\n')
    else:
        print('[-] The received file may be corrupted.')
    s.close()

if __name__ == '__main__':
    try:
        s = make_connection(host,port)
        recv_file(s)
    except Exception as e:
        s.close()
        print('[-]',e)