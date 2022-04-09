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
            FillRevisionFileInfo(r, svnPath)
    
        # iterate to next day
        startDateFormat += datetime.timedelta(days=1)
    
    return 

def main():
    
    # init logging
    logging.basicConfig(filename='errros.log', encoding='utf-8', level=logging.DEBUG)

    # init db
    dbcommands.initDb(config.dbserver, config.db)

    # main thread
    fillRevisionFilesInfo(config.startDate, config.endDate, config.svnPath)


if __name__ == '__main__':
    main()
