import subprocess
import datetime
import os

import svncommands
import parsers
import dbcommands

validArch = ['zip','rar']

def fillRevisionFilesInfo(startDate, endDate, svnPath):
    global validArch

    startDateFormat = datetime.datetime.strptime(startDate,'%Y-%m-%d')
    endDateFormat   = datetime.datetime.strptime(endDate,'%Y-%m-%d')

    while startDateFormat <= endDateFormat:

        examineStrDate = datetime.datetime.strftime(startDateFormat,'%Y-%m-%d')
        print('debug: the examine date - ', examineStrDate)

        # get revisions for one day
        revisionsForProcess = dbcommands.getRevisionsForProcess(examineStrDate)
        print('debug: revisions for this date - ', revisionsForProcess)

        # get info about all files affected by each revison
        for r in revisionsForProcess:
            print('debug: looking for revision - ', r)
            dbData = []

            # get list of files
            svnCommand = svncommands.commandGetListOfFiles(r, svnPath)
            svnCommandResult = svncommands.execute(svnCommand)
            listOfFiles = parsers.getListOfFiles(svnCommandResult)

            # for each file create record info ['guid', 'revision', 'attribure', 'filename', 'fileExtension', 'isArchive', 'filePath', 'pathToArchive']
            for l in listOfFiles:
                print('debug:   file information - ', l)
                fileInfo = parsers.parseSingleFile(l)
                fileInfo['revision'] = r
                print('debug:   fileInfo - ', fileInfo)
                if fileInfo['fileExtension'] in validArch:
                    fileInfo['isArchive'] = True
                    if fileInfo['fileAttribute'] != 'D':
                        print('debug:   need unpack archive')
                        archiveFileInfos = parsers.parseArchive(r, fileInfo, svnPath)
                        for a in archiveFileInfos:
                            print('debug:      archive file info', a)
                            dbData.append(a)
                    else:
                        dbData.append(fileInfo)    
                else:
                    fileInfo['isArchive'] = False
                    print('debug:   info is ready')
                    dbData.append(fileInfo)
        
        # iterate to next day
        startDateFormat += datetime.timedelta(days=1)
    
    return 

def main():
    
    # config
    svnPath = 'svn://172.20.1.17/ksu_mc21'

    dbserver = 'DESKTOP-V1FKJG7\SQLEXPRESS'    
    db = 'FCS'
    dbcommands.initDb(dbserver, db)

    startDate = '2022-04-01'
    endDate   = '2022-04-01' 
    
    # main thread
    fillRevisionFilesInfo(startDate, endDate, svnPath)

if __name__ == '__main__':
    main()
