import socket
import utils
import time
import sys
import os


def honey(port, run_time, verbose, reply):
    date, local_time = utils.create_timestamp()
    banner = 'Honey pot created [port %d] - %s %s\n' % (port, local_time, date)
    if verbose:
        print banner

    log_file = date.replace('/','')+'_'+local_time.split(':')[0]+local_time.split(':')[1]+'.log'
    open(log_file, 'wb').write(banner)
    s = utils.start_listener(port, 5)
    tic = time.time()
    try:
        while (time.time() - tic) < run_time:
            client, client_adr = s.accept()
            try:
                client.send(reply)
                client.close()
            except socket.error:
                print '[*] Connection Broken with %s' % client_adr[0]
            msg = '[*] Connection accepted-> %s:%d\n' % (client_adr[0], client_adr[1])
            if verbose:
                print msg
            open(log_file, 'a').write(msg)

    except KeyboardInterrupt:
        print '[!!] Server Killed [%ss Elapsed]' % str(time.time() - tic)
        pass
    s.close()


if 'basic' in sys.argv:
    start = time.time()
    cmd = 'cat index.html | nc -v -l -k 80'
    try:
        os.system(cmd)
    except KeyboardInterrupt:
        pass
    print '[!] Server Killed [%ss Elapsed]' % str(time.time()-tic)

if 'http' in sys.argv:
    honey(80, 60, True, open('index.html').read())

if 'ssh' in sys.argv:
    honey(22, 60, True, '\033[31m')

