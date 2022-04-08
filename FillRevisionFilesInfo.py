import subprocess
import datetime
import os
import uuid

import svncommands
import parsers
import dbcommands
import FillRevisionFileInfo

def fillRevisionFilesInfo(startDate, endDate, svnPath):

    startDateFormat = datetime.datetime.strptime(startDate,'%Y-%m-%d')
    endDateFormat   = datetime.datetime.strptime(endDate,'%Y-%m-%d')

    while startDateFormat <= endDateFormat:

        examineStrDate = datetime.datetime.strftime(startDateFormat,'%Y-%m-%d')

        # get revisions for one day
        revisionsForProcess = dbcommands.getRevisionsForProcess(examineStrDate)

        # get info about all files affected by each revison
        for r in revisionsForProcess:
            FillRevisionFileInfo.FillRevisionFileInfo(r, svnPath)
    
        # iterate to next day
        startDateFormat += datetime.timedelta(days=1)
    
    return 

def main():
    
    # config
    svnPath = 'svn://172.20.1.17/ksu_mc21'

    dbserver = 'DESKTOP-V1FKJG7\SQLEXPRESS'    
    db = 'FCS'
    dbcommands.initDb(dbserver, db)

    startDate = '2022-01-01'
    endDate   = '2022-04-06' 
    
    # main thread
    fillRevisionFilesInfo(startDate, endDate, svnPath)

if __name__ == '__main__':
    main()
