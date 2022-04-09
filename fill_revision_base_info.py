import datetime

import config
import svncommands
import parsers
import dbcommands

def fillRevisionBaseInfo(svnPath, startDate, endDate):

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

    dbcommands.initDb(config.dbserver, config.db)
    
    # main thread
    fillRevisionBaseInfo(config.svnPath, config.startDate, config.endDate)

if __name__ == '__main__':
    main()
