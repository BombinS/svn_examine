import sys
import os
import subprocess
import datetime
from typing import Text
import pyodbc

validArch = ['zip','rar']
svnPath = 'svn://172.20.1.17/ksu_mc21'

def getDbCursor(db):
    dbserver = 'DESKTOP-V1FKJG7\SQLEXPRESS'
    connectionString = 'DRIVER={ODBC Driver 13 for SQL Server};SERVER='+dbserver+';DATABASE='+db+';Trusted_Connection=yes'
    cnxn = pyodbc.connect(connectionString)
    cursor = cnxn.cursor()
    return cursor

def getSvnCommandGetListOfFiles(revision):
    """ Return the svn command for 
    """
    command = "svn log -r {} -v {}".format(revision, svnPath)
    return command

def executeGetListOfFiles(command):
    p = subprocess.run(command, capture_output=True, text=True)
    if p.returncode != 0:
        print(p.stderr)
        return
    else:
        return p.stdout

def parseArchive(filePath, fileName, fileExtension):
    if not os.path.isdir('./workspace'):
        os.makedirs('./workspace')
    result = []
    svnCommand = 'svn export {}{}/{}.{} ./workspace/{}.{}'.format(svnPath, filePath, fileName, fileExtension, fileName, fileExtension)
    p = subprocess.run(svnCommand, capture_output=True, text=True)    
    if p.returncode != 0:
        print(p.stderr)
    else:
        osCommand = 'unzip -l ./workspace/{}.{}'.format(fileName, fileExtension)
        p = subprocess.run(osCommand, capture_output=True, text=True)
        if p.returncode != 0:
            print(p.stderr)
        else:
            for s in p.stdout.splitlines():
                print('+++   ', s)
        # os.remove('./workspace/{}.{}'.format(fileName, fileExtension))
    return result

def parseFile(s):
    result = []
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
    if fileExtension in validArch:
        archiveFiles = parseArchive(filePath, fileName, fileExtension)
        for a in archiveFiles:
            result.append(a)
    # else:

    return result

def parseListOfFiles(textBuf):
    result = []
    isProcessing = False
    for s in textBuf.splitlines():
        if isProcessing == False and 'Changed paths:' in s:
            isProcessing = True
            continue
        if isProcessing == True:
            # exit processing on empty line
            if not s:
                break
            # process only files
            if ('.' in s[-9:]):
                result.append(parseFile(s))
            # splitted = s.strip().split('/')
            # fileAttribute = splitted[0]
            # del splitted[0]
            # fileFullPath = '/' + '/'.join(splitted)
            # splitted = fileFullPath.split('/')
            # fileName = splitted[-1]
            # splitted.pop()
            # filePath = '/'.join(splitted)
            # if ('.' in fileName[-9:]):
            #     fileExtension = fileName.split('.')[1]
            #     if fileExtension in validArch:
            #         print('need unpack - ', fileFullPath)
            #     else:
            #         print('ready to process - path: {} | name {}'.format( filePath, fileName))
            # else:                
            #     print('skip - ', fileName)
    return result

# добавить запись в словарь (ревизия : информация о ревизии - автор, время)
def parseBaseRevisionInfo(s, d):
    values = list(map(str.strip, s.split('|')))
    d[values[0]] = [values[1], values[2]]
    return d

def addBaseRevisionRecord(cursor, id, values):
    """ Add record about base revision info to db  

    id: revision id
    values[0]: author
    values[1]: date

    """
    sqlQuery = 'select * from RevisionBaseInfo where id = {}{}{}'.format("'",id,"'")
    cursor.execute(sqlQuery)
    row = cursor.fetchone() 
    if not row:
        sqlQueryHeaders = '([Id], [Author], [Date], [isFilesProcceed])'
        sqlQueryValues = "('{}', '{}', '{}', 0)".format(id, values[0], values[1].split(' +')[0])
        sqlQuery = 'insert into [FCS].[dbo].[RevisionBaseInfo] {} values {}'.format(sqlQueryHeaders, sqlQueryValues)
        cursor.execute(sqlQuery)
        cursor.commit()

def getRevisionsForProcess(cursor, examineStrDate):
    result = []
    sqlQuery = "select * from RevisionBaseInfo where cast(Date as Date)='{}' and isFilesProcceed=0".format(examineStrDate)
    cursor.execute(sqlQuery)
    row = cursor.fetchone()
    while row:
        result.append(row[0])
        row = cursor.fetchone()
    return result

def fillRevisionFilesInfo(startDate, endDate, db):

    # global instance - cursor to db
    cursor = getDbCursor(db)

    startDateFormat = datetime.datetime.strptime(startDate,'%Y-%m-%d')
    endDateFormat   = datetime.datetime.strptime(endDate,'%Y-%m-%d')

    while startDateFormat <= endDateFormat:

        examineStrDate = datetime.datetime.strftime(startDateFormat,'%Y-%m-%d')
        
        revisionsForProcess = []
        revisionsForProcess = getRevisionsForProcess(cursor, examineStrDate)

        for r in revisionsForProcess:
            svnCommand = getSvnCommandGetListOfFiles(r)
            svnCommandResult = executeGetListOfFiles(svnCommand)
            listOfFiles = []
            listOfFiles = parseListOfFiles(svnCommandResult)

        startDateFormat += datetime.timedelta(days=1)

    return 

def main():
    
    db = 'FCS'
    startDate = '2022-03-29'
    endDate   = '2022-03-29' 

    # main thread
    fillRevisionFilesInfo(startDate, endDate, db)

if __name__ == '__main__':
    main()
