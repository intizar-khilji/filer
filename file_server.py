# A file transfer program called [FILER 0.2.1]
# (c) Intzaar
# File Transfer using python3
# file_server 0.2
# ----------Variables--------------
host = ''
port = 9999
buffer = 64
seperator_len = 30
# ---------------------------------

print('-'*seperator_len+'\n\tFILER\n'+'-'*seperator_len)
# Python imports
import socket, os, sys
# Finding IP address
try:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as f:
        f.connect(('8.8.8.8',53))
        print('-'*seperator_len+'\nHost IP Address :',f.getsockname()[0]+'\n'+'-'*seperator_len+'\n')
except:
    print('-'*seperator_len+'\nYou are not connected yet\nLocalhost IP - 127.0.0.1')

# Manage command line arguments
args = sys.argv
if len(args) == 1:
    print('-'*seperator_len+'\nargs[1] - File Name\nargs[2] - Buffer Size\n'+'-'*seperator_len)
    sys.exit()
elif len(args) == 2:
    file = args[1]
elif len(args) == 3:
    file = args[1]
    buffer = int(args[2])

# Projgress Bar
def progress(count, total):
    status = ''
    bar_len = 50
    filled_len = int(round(bar_len * count / float(total)))
    percents = round(100.0 * count / float(total), 1)
    bar = '#' * filled_len + '.' * (bar_len - filled_len)
    if percents < 100:
        status = 'Transfering...'
    else:
        status = 'Done.           '
    sys.stdout.write('[%s] %s%s | %s\r' % (bar, percents, '%', status))
    sys.stdout.flush()

# Make connection
def make_connection(host,port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(20)
    s.bind((host,port))
    s.listen(1)
    print('[+] Waiting for connection...')
    c,addr = s.accept()
    print('Connected with',addr[0], addr[1])
    c.send(b'[+] Connection established.')
    return c

# File transfer logic
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
        try:
            c.close()
        except:
            print('[-] Not Connected.')
        print('[-]',e)