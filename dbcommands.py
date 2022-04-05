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
        sqlQuery = 'insert into [FCS].[dbo].[RevisionBaseInfo] {} values {}'.format(sqlQueryHeaders, sqlQueryValues)
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

def markBaseRevisionProceed(rev):
    sqlQuery = "update [dbo].[RevisionBaseInfo] set isFilesProcceed = 1 where Id = '{}'".format(rev)
    cursor.execute(sqlQuery)
    cursor.commit()


