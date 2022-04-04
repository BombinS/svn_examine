from asyncio.windows_events import NULL
from fileinput import filename
import subprocess
from unittest import result

def main(path):
    command = 'unzip -l {}'.format(path)
    p = subprocess.run(command, capture_output=True, text=True)
    buf = []
    if p.returncode != 0:
        print(p.stderr)
        exit()
    else:
        buf = p.stdout.splitlines()
        print(p.stdout)
    
    isStart = False
    result = []
    for s in buf:
        if isStart == True and '---' in s:
            break
        if '---' in s:
            isStart= True
            continue
        if isStart == True:
            splitted = s.split('  ')
            length = splitted[-3].strip()
            fullFileName = splitted[-1].strip()
            if (length != '0'):
                splitted = fullFileName.split('/')
                if len(splitted) == 1:
                    result.append([NULL, splitted[0]])
                else:
                    fileName = splitted.pop()
                    filePath = '/'.join(splitted)
                    result.append([filePath, fileName])
    for r in result:
        print(r)


if __name__ == '__main__':
    main('workspace/LLT_MC21_FCS_ACE11L_PJ08_PC031_DOWN_RES.zip')