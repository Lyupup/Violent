import zipfile
import time
from threading import Thread
import optparse

def extractFile(zfile,password):
    try:
        zfile.extractall(pwd=str.encode(password))
        print("password  is : %s" % password)
        print(time.time())
        return
    except:
        pass


def main():
    parser = optparse.OptionParser("Usage%prog -f <zipfile> -d <dictionary>")
    parser.add_option('-f', dest='zname', type='string', help='specify zip file')
    parser.add_option('-d', dest='dname', type='string', help='specify dictionary file')
    (options,args) = parser.parse_args()
    if (options.zname == None) | (options.dname == None):
        print(parser.usage)
        exit(0)
    else:
        zname = options.zname
        dname = options.dname

    zfile = zipfile.ZipFile(zname)
    passfile = open(dname)
    print(time.time())
    for line in passfile.readlines():
        line = line.strip('\n')
        # extractFile(zfile,line)
        t = Thread(target=extractFile,args=(zfile,line))
        t.start()
    print(time.time())
if __name__ == '__main__':
    main()