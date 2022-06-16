from distutils.command.config import config
import uuid
import logging

import svncommands
import parsers
import dbcommands
import config


validArch = ['zip','rar']

def FillRevisionFileInfo(r, svnPath):

    dbData = []

    # get list of files
    svnCommand = svncommands.commandGetListOfFiles(r, svnPath)
    svnCommandResult = svncommands.execute(svnCommand)
    listOfFiles = parsers.getListOfFiles(svnCommandResult)

    # for each file create record info ['guid', 'revision', 'attribure', 'filename', 'fileExtension', 'filePath', 'pathArchive', 'isArchive']
    for l in listOfFiles:
        fileInfo = parsers.parseSingleFile(l)
        fileInfo['revision'] = r
        if fileInfo['fileExtension'] in validArch:
            fileInfo['isArchive'] = True
            if fileInfo['fileAttribute'] != 'D':
                archiveFileInfos = parsers.parseArchive(r, fileInfo, svnPath)
                for a in archiveFileInfos:
                    acrchiveFileInfo = {}
                    acrchiveFileInfo['isArchive'] = fileInfo['isArchive']
                    acrchiveFileInfo['UUID'] = uuid.uuid1()
                    acrchiveFileInfo['fileAttribute'] = fileInfo['fileAttribute']
                    acrchiveFileInfo['revision'] = fileInfo['revision']
                    acrchiveFileInfo['fileName'] = a[1]
                    if len(a) > 2:
                        acrchiveFileInfo['fileExtension'] = a[2]
                    acrchiveFileInfo['filePath'] = '{}/{}.{}'.format(fileInfo['filePath'], fileInfo['fileName'], fileInfo['fileExtension'])
                    acrchiveFileInfo['pathArchive'] = a[0]
                    dbData.append(acrchiveFileInfo)
            else:
                fileInfo['pathArchive'] = ''
                fileInfo['UUID'] = uuid.uuid1()                        
                dbData.append(fileInfo)    
        else:
            fileInfo['isArchive'] = False
            fileInfo['pathArchive'] = ''
            fileInfo['UUID'] = uuid.uuid1()
            dbData.append(fileInfo)                
        
    # add record to Db
    dbcommands.addFileInfoRecord(dbData)

    # mark revison as processed
    dbcommands.markBaseRevisionProceed(r)

    return

if __name__ == '__main__':
    # debug
    logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
    FillRevisionFileInfo("r18138", config.svnPath)
