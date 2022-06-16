from fileinput import filename
import logging
from asyncio.windows_events import NULL
import pyodbc

cursor = NULL

def initDb(dbserver, db):
    global cursor
    connectionString = 'DRIVER={ODBC Driver 13 for SQL Server};SERVER='+dbserver+';DATABASE='+db+';Trusted_Connection=yes'
    cnxn = pyodbc.connect(connectionString)
    cursor = cnxn.cursor()

def addBaseRevisionRecord(id, values):
    """ Add record about base revision info to db  
        id: revision id
        values[0]: author
        values[1]: date
    """
    global cursor
    sqlQuery = 'select * from RevisionBaseInfo where id = {}{}{}'.format("'",id,"'")
    cursor.execute(sqlQuery)
    row = cursor.fetchone() 
    if not row:
        sqlQueryHeaders = '([Id], [Author], [Date], [isFilesProcceed])'
        sqlQueryValues = "('{}', '{}', '{}', 0)".format(id, values[0], values[1].split(' +')[0])
        sqlQuery = 'insert into RevisionBaseInfo {} values {}'.format(sqlQueryHeaders, sqlQueryValues)
        cursor.execute(sqlQuery)
        cursor.commit()

def addFileInfoRecord(records):
    """ 
    """
    global cursor
    for record in records:
        sqlQueryHeaders = "([id], [revision], [filename], [extension], [mode], [path], [patharchive], [isArchive])"
    
        fileExtension = ''
        if 'fileExtension' in record:
            fileExtension = record['fileExtension']

        sqlQueryValues = "('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(
            record['UUID'], 
            record['revision'], 
            record['fileName'], 
            fileExtension, 
            record['fileAttribute'], 
            record['filePath'], 
            record['pathArchive'], 
            record['isArchive'])

        sqlQuery = 'insert into [dbo].[RevisionFileInfo] {} values {}'.format(sqlQueryHeaders, sqlQueryValues)
        cursor.execute(sqlQuery)
        cursor.commit()

def getRevisionsForProcess(examineStrDate):
    global cursor
    result = []
    sqlQuery = "select * from RevisionBaseInfo where cast(Date as Date)='{}' and isFilesProcceed=0".format(examineStrDate)
    cursor.execute(sqlQuery)
    row = cursor.fetchone()
    while row:
        result.append(row[0])
        row = cursor.fetchone()
    return result

def getFileInfo(fileName, extension, revision):
    global cursor
    sqlQuery = "select count(*) from RevisionFileInfo where filename='{}' and extension='{}' and revision='{}'".format(fileName, extension, revision)
    cursor.execute(sqlQuery)
    n = cursor.fetchone()[0]
    if (n != 1):
        logging.error("filename - {}.{}, revision - {}. Expect 1 recond, but found {}".format(fileName, extension, revision, n))
        return {}
    # вернуть [архив?, имя файла, расширение файлаб путь к svn, путь в архиве]
    sqlQuery = "select isArchive, filename, extension, path, patharchive from RevisionFileInfo where filename='{}' and extension='{}' and revision='{}'".format(fileName, extension, revision)
    cursor.execute(sqlQuery)
    row = cursor.fetchone()
    fileInfo = {}
    fileInfo['isArchive'] = row[0]
    fileInfo['fileName'] = "{}.{}".format(row[1], row[2])
    fileInfo['svnPath'] = row[3]
    if row[4]:
        fileInfo['archivePath'] = row[4]
    return fileInfo

def getDistinctScadeFileNames(target, extension):
    global cursor
    sqlQuery = "SELECT distinct (filename)\
        FROM RevisionFileInfo\
        where extension = '{}' and path like '%IVVPr_{}/Tests/Developing/Testing_Procedures_for_SCADE%'".format(extension, target)
    cursor.execute(sqlQuery)
    result = []
    row = cursor.fetchone()
    while row:
        result.append(row[0])
        row = cursor.fetchone()
    return result    

def getLastScadeFilenameInfo(target, extension, filename):
    global cursor
    sqlQuery = "SELECT TOP 1 fi.revision, fi.path, ri.Date, ri.Author\
        FROM RevisionFileInfo fi\
        join RevisionBaseInfo ri on fi.revision = ri.Id\
        where extension = '{}' and path like '%IVVPr_{}/Tests/Developing/Testing_Procedures_for_SCADE%' and filename = '{}'\
        order by ri.Date desc".format(extension, target, filename)
    cursor.execute(sqlQuery)
    row = cursor.fetchone()
    if row:
        return [row[0], row[1], row[2], row[3]]
    return []


def markBaseRevisionProceed(rev):
    sqlQuery = "update [dbo].[RevisionBaseInfo] set isFilesProcceed = 1 where Id = '{}'".format(rev)
    cursor.execute(sqlQuery)
    cursor.commit()



