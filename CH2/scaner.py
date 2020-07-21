import optparse
import socket
from socket import *
from threading import *
screenLock = Semaphore(value=1)

def connScan(tgtHost,tgtPort):
    try:
        connSkt = socket(AF_INET, SOCK_STREAM)
        connSkt.connect((tgtHost,int(tgtPort)))
        connSkt.send(b"Hahahahahaha\r\n")
        res = str(connSkt.recv(1024))
        print(len(res))
        screenLock.acquire()
        print('[+] %s/tcp open' %tgtPort)
        print('[+] '+ str(res))
    except:
        screenLock.acquire()
        print('[-] %s/tcp closed' %tgtPort)
    finally:
        screenLock.release()
        connSkt.close()



def portScan(tgtHost,tgtPorts):
    try:
        tgtip = gethostbyname(tgtHost)
    except:
        print("[-] Cannot resolve '%s': Unknow host" %tgtHost)
    try:
        tgtName = gethostbyaddr(tgtip)
        print('[+] Scan Results for :' + tgtName[0])
    except:
        print('[+] Scan Results for:' + tgtip)
    setdefaulttimeout(1)
    tgtPorts = tgtPorts.split(',')
    for tgtPort in tgtPorts:
        t = Thread(target=connScan,args=(tgtHost,int(tgtPort)))
        t.start()



def main():
    pareser = optparse.OptionParser('Usage %Prog -H <target host> -p <target port>')
    pareser.add_option('-H',dest='tgtHost',type='string',help='specify target host')
    pareser.add_option('-p', dest='tgtPort', type='string', help='specify target post')
    (options,args) = pareser.parse_args()
    tgtHost = options.tgtHost
    tgtPort = options.tgtPort
    if (tgtHost == None) or (tgtPort == None):
        print(pareser.usage)
        exit(0)
    portScan(tgtHost,tgtPort)
if __name__ == '__main__':
    main()
