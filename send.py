# A file transfer program called [FILER 1.0]
# (c) Intzaar
# File Transfer using python3
# file_server 1.0
# Date - 02-08-2020
# ----------Variables--------------
host = ''
port = 9999
buffer = 64
seperator_len = 30
files = []
timeout = 20
version = 1.0
encode_type = 'utf-8'
# Python imports
import socket, os, sys, argparse

# Get Specific Extension file
def listfile(file, ext):
    ext_len = len(ext)
    if '.'+ext == file[-ext_len-1:]:
        return True
    return False
# Manage command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-f','--filename', nargs='+', help='Specify file (one or more than one.)')
parser.add_argument('-b', '--buffer', help='Enter custom buffer size', type=int)
parser.add_argument('-p', '--port', help='Port Number', type=int)
parser.add_argument('--timeout', help='Set timeout in sec', type=int)
parser.add_argument('--version', help='Get current version', action='store_true')
args = parser.parse_args()
if args.filename:
    if '*' in args.filename[0]:
        if '*.*' == args.filename[0]:
            files = [i for i in os.listdir() if os.path.isfile(i)]
        else:
            # ext = args.filename[0][args.filename[0].rindex('.')+1:]
            ext = os.path.splitext(args.filename[0])
            files = [i for i in os.listdir() if listfile(i, ext)]
    else:
        files = args.filename
if args.filename is None and not args.version:
    parser.print_help()
    sys.exit()
if args.buffer:
    buffer = args.buffer
if args.port:
    port = args.port
if args.timeout:
    timeout=args.timeout
if args.version:
    print(version)
    sys.exit()
# ---------------------------------

print('-'*seperator_len+'\n\tFILER\n'+'-'*seperator_len)
# Finding IP address
try:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as f:
        f.connect(('8.8.8.8',53))
        print('-'*seperator_len+'\nHost IP Address :',f.getsockname()[0]+'\n'+'-'*seperator_len+'\n')
except:
    print('-'*seperator_len+'\nYou are not connected yet\nLocalhost IP - 127.0.0.1')

# Progress Bar
def progress(count, total):
    status = ''
    bar_len = os.get_terminal_size()[0]-30
    filled_len = int(round(bar_len * count / float(total)))
    percents = round(100.0 * count / float(total), 1)
    bar = '#' * filled_len + '.' * (bar_len - filled_len)
    if percents < 100:
        status = 'Sending...'
    else:
        status = 'Done.           '
    sys.stdout.write('[%s] %s%s | %s\r' % (bar, percents, '%', status))
    sys.stdout.flush()

# Make connection
def make_connection(host,port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
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
    info_len = str(len(info))
    info_len = ' '*(4-len(info_len))+info_len
    c.send(info_len.encode())
    c.send(info.encode())
    print('Name :',basename,'\nSize :',filesize,'bytes')
    with open(file, 'rb') as f:
        for i in range((filesize//buffer)+1):
            progress(i,(filesize//buffer)+1)
            line = f.read(buffer)
            c.send(line)
        print()
    try:
        ack = c.recv(3).decode()
        if ack == 'ack':
            print('[+] File Transfered.\n')
    except Exception as e:
        print('[-] Acknowledgement not received.\n'+e)

def main():
        try:
            c = make_connection(host,port)
            number_of_files = str(len(files))
            number_of_files = ' '*(4-len(number_of_files))+number_of_files
            print('[+] Number of files :', number_of_files)
            c.send(number_of_files.encode())
            for file in files:
                send_file(c,file,buffer)
            c.close()
        except Exception as e:
            try:
                c.close()
            except:
                print('[-] Not Connected.')
            print('[-]',e)

if __name__ == '__main__':
    main()