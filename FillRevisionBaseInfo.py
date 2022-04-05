import subprocess
import datetime

import svncommands
import parsers
import dbcommands

def fillRevisionBaseInfo(svnPath, startDate, endDate):

    # # global instance - cursor to db
    # cursor = getDbCursor(db)

    startDateFormat = datetime.datetime.strptime(startDate,'%Y-%m-%d')
    endDateFormat   = datetime.datetime.strptime(endDate,'%Y-%m-%d')

    while startDateFormat <= endDateFormat:

        examineStrDate = datetime.datetime.strftime(startDateFormat,'%Y-%m-%d')

        # form svn command to get logs by day
        command = svncommands.commandGetRevisionsByDate(svnPath, examineStrDate)

        # execute svn command
        svnCommandResult = svncommands.execute(command)

        # get base info about revision (format - dictionary {'revision': [author, datetame]})
        dict = parsers.getBaseRevisionInfo(svnCommandResult, examineStrDate)

        # fill db by base revision info for this day
        for k, v in dict.items():
            dbcommands.addBaseRevisionRecord(k, v)

        # iterate to next day
        startDateFormat += datetime.timedelta(days=1)

    return 0


def main():

    # config
    svnPath = 'svn://172.20.1.17/ksu_mc21'

    dbserver = 'DESKTOP-V1FKJG7\SQLEXPRESS'    
    db = 'FCS'
    dbcommands.initDb(dbserver, db)

    startDate = '2022-01-01'
    endDate   = '2022-04-06' 
    
    # main thread
    fillRevisionBaseInfo(svnPath, startDate, endDate)

if __name__ == '__main__':
    main()
