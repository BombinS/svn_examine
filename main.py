from base64 import decode, encode
from cgitb import text
import subprocess

svnPath = 'svn://172.20.1.17/ksu_mc21'

def main():
    command = 'svn info' + ' ' + svnPath 
    p = subprocess.run(command, capture_output=True, text=True)
    result = p.stdout.splitlines()
    print(result)
    f = open("i.info","w")
    f.write(p.stdout)
    f.close()



if __name__ == '__main__':
    main()
