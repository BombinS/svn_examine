import os
import subprocess
import svncommands

def getBaseRevisionInfo(buf, examineStrDate):
    """
        get base info about revision as dictionary {'revision': [author, datetame]})
    """
    dict = {}
    for s in buf:
        if s.startswith('r'):
            if examineStrDate in s:
                values = list(map(str.strip, s.split('|')))
                dict[values[0]] = [values[1], values[2]]
    return dict

def parseArchive(revision, fileInfo, svnPath):
    #prepare work directory
    if not os.path.isdir('./workspace'):
        os.makedirs('./workspace')

    # export archive
    command = svncommands.commandExportArchive(revision, svnPath, fileInfo['filePath'], fileInfo['fileName'], fileInfo['fileExtension'])
    svncommands.execute(command)

    # show files at archive
    osCommand = "unzip -l './workspace/{}.{}'".format(fileInfo['fileName'], fileInfo['fileExtension'])
    p = subprocess.run(osCommand, capture_output=True, text=True)
    if p.returncode != 0:
        print(p.stderr)
        return []
    else:
        result = []
        isStart = False
        for s in p.stdout.splitlines():
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
                        fileNameWithExtentsion = splitted[0]
                        fileNameWithExtentsionSplitted = fileNameWithExtentsion.split('.')
                        result.append(['', fileNameWithExtentsionSplitted[0],fileNameWithExtentsionSplitted[1]])
                    else:
                        fileNameWithExtentsion = splitted.pop()
                        fileNameWithExtentsionSplitted = fileNameWithExtentsion.split('.')
                        filePath = '/'.join(splitted)
                        if len(fileNameWithExtentsionSplitted) == 1:
                            result.append([filePath, fileNameWithExtentsionSplitted[0]])
                        else:
                            result.append([filePath, fileNameWithExtentsionSplitted[0], fileNameWithExtentsionSplitted[1]])
        # os.remove('./workspace/{}.{}'.format(fileInfo['fileName'], fileInfo['fileExtension']))
        return result

def parseSingleFile(s):
    result = {}
    s = s.strip()
    splitted = s.split('/')
    fileAttribute = splitted[0].strip()
    fileName = splitted[-1]
    splitted.pop()
    splitted.pop(0)
    filePath = '/' + '/'.join(splitted)
    splitted = fileName.split('.')
    fileExtension = splitted[-1].lower()
    splitted.pop()
    fileName = ''.join(splitted)
    result['fileName'] = fileName
    result['fileAttribute'] = fileAttribute
    result['fileExtension'] = fileExtension
    result['filePath'] = filePath
    return result

def getListOfFiles(buf):
    result = []
    isProcessing = False
    for s in buf:
        # the label for start processing is next line after 'Changed paths'
        if isProcessing == False and 'Changed paths:' in s:
            isProcessing = True
            continue
        if isProcessing == True:
            # exit processing on empty line
            if not s:
                break
            # process only files
            if ('.' in s[-9:]):                
                # result.append(parseSingleFile(s))
                result.append(s)
    return result


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
    


if __name__ == '__main__':
    main('workspace/LLT_MC21_FCS_ACE11L_PJ08_PC031_DOWN_RES.zip')