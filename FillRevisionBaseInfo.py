from optparse import Values
import sys
import subprocess
import datetime
import pyodbc

def getDbCursor(db):
    dbserver = 'DESKTOP-V1FKJG7\SQLEXPRESS'
    connectionString = 'DRIVER={ODBC Driver 13 for SQL Server};SERVER='+dbserver+';DATABASE='+db+';Trusted_Connection=yes'
    cnxn = pyodbc.connect(connectionString)
    cursor = cnxn.cursor()
    return cursor

def getRevisionsByDateCommand(svnPath, date):
    """ Return the svn command for getting the list of commits to repo for some day 
    
    example: 
       |  input | 2022-03-24
       | output | svn log -r {2022-03-24}:{2022-03-25} svn://172.20.1.17/ksu_mc21

    """
    dateStart = datetime.datetime.strptime(date,'%Y-%m-%d')
    dateEnd = dateStart + datetime.timedelta(days=1)
    s1 = datetime.datetime.strftime(dateStart,'%Y-%m-%d')
    s2 = datetime.datetime.strftime(dateEnd,'%Y-%m-%d')
    command = "svn log -r {}:{} {}".format('{' + s1 + '}','{' + s2 + '}', svnPath)
    return command

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

def fillRevisionBaseInfo(svnPath, startDate, endDate, db):

    # global instance - cursor to db
    cursor = getDbCursor(db)

    startDateFormat = datetime.datetime.strptime(startDate,'%Y-%m-%d')
    endDateFormat   = datetime.datetime.strptime(endDate,'%Y-%m-%d')

    while startDateFormat <= endDateFormat:

        examineStrDate = datetime.datetime.strftime(startDateFormat,'%Y-%m-%d')

        # form svn command to get logs by day
        command = getRevisionsByDateCommand(svnPath, examineStrDate)

        # execute svn command
        p = subprocess.run(command, capture_output=True, text=True)

        # hanldle errors
        if (p.returncode != 0):
            print(p.stderr)
        
        # handle success
        else:
            # fill dictionary {revision : [author, datetime]}
            dict = {}
            for s in p.stdout.splitlines():
                if s.startswith('r'):
                    if examineStrDate in s:
                        parseBaseRevisionInfo(s, dict)

            # fill db
            for k, v in dict.items():
                addBaseRevisionRecord(cursor, k, v)

            # for k, v in dict.items():
            #     command = 'svn log -r {} -v svn://172.20.1.17/ksu_mc21'.format(k, svnPath)
            #     p = subprocess.run(command, capture_output=True, text=True)
            #     print(p.stdout)

        startDateFormat += datetime.timedelta(days=1)

    return 0

def main():

    # config
    svnPath = 'svn://172.20.1.17/ksu_mc21'
    startDate = '2022-01-01'
    endDate   = '2022-04-01' 
    db = 'FCS'

    # main thread
    fillRevisionBaseInfo(svnPath, startDate, endDate, db)

if __name__ == '__main__':
    main()
