import datetime
import subprocess
import logging

def commandGetRevisionsByDate(svnPath, date):
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

def commandGetListOfFiles(revision, svnPath):
    """ Return the svn command for 
    """
    command = "svn log -r {} -v {}".format(revision, svnPath)
    return command

def commandExportArchive(revision, svnPath, filePath, fileName, fileExtension):
    command = 'svn export -r {} "{}{}/{}.{}" "./workspace/{}.{}"'.format(revision, svnPath, filePath, fileName, fileExtension, fileName, fileExtension)
    return command


def execute(command):
    p = subprocess.run(command, capture_output=True, text=True)
    if (p.returncode != 0):
        logging.error(p.stderr)
        return
    else:
        return p.stdout.splitlines()


  