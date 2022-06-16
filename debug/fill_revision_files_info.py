import datetime
import logging


import dbcommands
import config
from fill_revision_file_info import FillRevisionFileInfo  

def fillRevisionFilesInfo(startDate, endDate, svnPath):

    startDateFormat = datetime.datetime.strptime(startDate,'%Y-%m-%d')
    endDateFormat   = datetime.datetime.strptime(endDate,'%Y-%m-%d')

    while startDateFormat <= endDateFormat:
    
        examineStrDate = datetime.datetime.strftime(startDateFormat,'%Y-%m-%d')

        # get revisions for one day
        revisionsForProcess = dbcommands.getRevisionsForProcess(examineStrDate)

        # get info about all files affected by each revison
        for r in revisionsForProcess:
            if (r not in 'r18138'
                and r not in 'r18690'
                and r not in 'r18883'
                and r not in 'r14027'
                and r not in 'r10337'
                and r not in 'r10728'
                and r not in 'r11255'
                and r not in 'r16981'
                and r not in 'r12351'
                and r not in 'r13395'
                and r not in 'r4384'
                and r not in 'r4511'
                and r not in 'r4526'
                and r not in 'r4534'
                and r not in 'r4543'
                and r not in 'r4631'
                and r not in 'r4632'
                ):
                    FillRevisionFileInfo(r, svnPath)
    
        # iterate to next day
        startDateFormat += datetime.timedelta(days=1)
    
    return 

def main():
    
    # init logging
    logging.basicConfig(filename='errors.log', encoding='utf-8', level=logging.DEBUG)

    # init db
    dbcommands.initDb(config.dbserver, config.db)

    # main thread
    fillRevisionFilesInfo(config.startDate, config.endDate, config.svnPath)


if __name__ == '__main__':
    main()
