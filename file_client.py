# A file transfer program called [FILER 0.2.1]
# (c) Intzaar
# File Transfer using python3
# file_client 0.2.1
# -----------Variables-------------
host = 'localhost'
port = 9999
path = ''
seperator_len = 30
# ---------------------------------

print('-'*seperator_len+'\n\tFILER\n'+'-'*seperator_len)
# Python imports
import socket, os, sys,time
# Manage command line arguments
args = sys.argv
if len(args)==2:
    host = args[1]
elif len(args)==3:
    host = args[1]
    path = args[2]
else:
    print('-'*seperator_len+'\nargs[1] - Host IP Address\nargs[2] - File Path\nDefault IP Address - localhost\n'+'-'*seperator_len)
# Progress Bar
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
# Establish connection
def make_connection(host,port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('[+] Waiting for server...')
    i,n = 0,5
    while i<n:
        try:
            s.connect((host, port))
            break
        except:
            sys.stdout.write('[-] Retrying('+str(i+1)+')...\r')
            sys.stdout.flush()
            time.sleep(0.5)
            i+=1
            if i == n:
                print('\n[-] Not connected.')
                sys.exit()
    print(s.recv(32).decode())
    return s
# File receiver logic
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
        for i in range((filesize//buffer)+1):
            progress(i,(filesize//buffer)+1)
            line = s.recv(buffer)
            f.write(line)
        print()
        f.seek(0)
        f.flush()
    filesize2 = os.path.getsize(file)
    if filesize == filesize2:
        s.send(b'ack')
        print('[+] Transmission Successfully Completed.\n')
    else:
        print('[-] The received file may be corrupted.')
        print('[-] Received File Size :',filesize2,'Bytes')
    s.close()

if __name__ == '__main__':
    try:
        s = make_connection(host,port)
        recv_file(s,path)
    except Exception as e:
        s.close()
        print('[-]',e)