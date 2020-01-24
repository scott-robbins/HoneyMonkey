import socket
import utils
import time
import sys
import os

log_timer = 30  # seconds between log updates


def honey(port, run_time, verbose, reply):
    clients = []
    date, local_time = utils.create_timestamp()
    banner = 'Honey pot created [port %d] - %s %s\n' % (port, local_time, date)
    if verbose:
        print 'Honey pot created [port %d] - %s %s' % (port, local_time, date)
        print '[*] Initialized Uptime: %f hours' % (run_time/3600.)
    data = ''
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
                clients.append(client_adr[0])
            except socket.error:
                print '[*] Connection Broken with %s' % client_adr[0]
            except:
                pass

            msg = '[*] Connection accepted-> %s:%d' % (client_adr[0], client_adr[1])
            data += '[*] Connection accepted from %s at %s - %s\n' % (client_adr[0], date, local_time)
            if verbose:
                print msg
            if int(time.time()-tic)%1==0:
                date, local_time = utils.create_timestamp()
            if int(time.time() - tic) % log_timer == 0:
                print '[*] Logging Connections [%ss Elapsed]' % str(time.time()-tic)
                open(log_file, 'wb').write(data)
                data = ''

    except KeyboardInterrupt:
        print '[!!] Server Killed [%ss Elapsed]' % str(time.time() - tic)
        pass
    s.close()


if 'basic' in sys.argv:
    start = time.time()
    try:
        os.system('sh serve.sh')
    except KeyboardInterrupt:
        pass
    print '[!] Server Killed [%ss Elapsed]' % str(time.time()-start)

if 'http' in sys.argv:
    honey(80, 1e5, True, open('templates/index.html').read())

if 'ssh' in sys.argv:
    honey(22, 60, True, '\033[31m')

