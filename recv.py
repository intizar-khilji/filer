# A file transfer program called [FILER 1.0]
# (c) Intzaar
# File Transfer using python3
# file_client 1.0
# Date - 02-08-2020
# -----------Variables-------------
host = 'localhost'
port = 9999
path = ''
seperator_len = 30
version = 1.0
# Python imports
import socket, os, sys,time, argparse
# Manage command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-u','--host', help='Host IP Address')
parser.add_argument('-p', '--port', help='Port Number', type=int)
parser.add_argument('-l', '--location', help='Receiver Directory')
parser.add_argument('--version', help='Get current version', action='store_true')
args = parser.parse_args()
if args.host:
    host = args.host
if args.host is None and not args.version:
    parser.print_help()
    sys.exit()
if args.port:
    port = args.port
if args.location:
    path = args.location
if args.version:
    print(version)
    sys.exit()
# ---------------------------------

print('-'*seperator_len+'\n\tFILER\n'+'-'*seperator_len)
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
    
def main():
        try:
            s = make_connection(host,port)
            number_of_files = int(s.recv(4).decode().strip())
            print('[+] Number of files :', number_of_files)
            for _ in range(number_of_files):
                recv_file(s,path)
        except Exception as e:
            s.close()
            print('[-]',e)
        s.close()

if __name__ == '__main__':
    main()