# (c) Intzaar
# File Transfer using python3
# file_server 0.2
# ---------------------------------
host = ''
port = 9999
buffer = 64
# ---------------------------------

import socket, os, sys

args = sys.argv
if len(args) == 1:
    print('args[1] - File Name\nargs[2] - Buffer Size')
    sys.exit()
elif len(args) == 2:
    file = args[1]
elif len(args) == 3:
    file = args[1]
    buffer = int(args[2])

def progress(count, total):
    status = ''
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '#' * filled_len + '.' * (bar_len - filled_len)
    if percents < 100:
        status = 'Transfering...'
    else:
        status = 'Done.           '
    sys.stdout.write('[%s] %s%s | %s\r' % (bar, percents, '%', status))
    sys.stdout.flush()

def make_connection(host,port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host,port))
    s.listen(1)
    print('[+] Waiting for connection...')
    c,addr = s.accept()
    print('Connected with',addr[0], addr[1])
    c.send(b'[+] Connection established.')
    return c

def send_file(c, file, buffer):
    sep='<SEP>'
    basename = os.path.basename(file)
    filesize = os.path.getsize(file)
    info = basename+sep+str(buffer)+sep+str(filesize)
    c.send(info.encode())
    print('Name :',basename,'\nSize :',filesize,'bytes')
    with open(file, 'rb') as f:
        for i in range((filesize//buffer)+1):
            progress(i,(filesize//buffer)+1)
            line = f.read(buffer)
            c.send(line)
        print()
    try:
        ack = c.recv(4).decode()
        if ack == 'ack':
            print('[+] File Transfered.\n')
    except Exception as e:
        print('[-] Acknowledgement not received.\n'+e)
    c.close()

if __name__ == '__main__':
    try:
        c = make_connection(host,port)
        send_file(c,file,buffer)
    except Exception as e:
        c.close()
        print('[-]',e)