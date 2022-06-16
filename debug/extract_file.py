from ast import walk
import logging
import os

import config
import dbcommands 
import svncommands

def main(fileName, extension, revision):

    # init logging
    logging.basicConfig(filename='extract_files.log', encoding='utf-8', level=logging.DEBUG)    

    # init DB
    dbcommands.initDb(config.dbserver, config.db)

    # get file info {'isArchive', 'fileName', 'svnPath', 'archivePath'
    fileInfo = dbcommands.getFileInfo(fileName, extension, revision)
    for k,v in fileInfo.items():
        print(k, v)

    if len(fileInfo) == 0:
        logging.error("{}.{} by revision {} is not obtained\n".format(fileName, extension, revision))
        return

    if fileInfo['isArchive']:
        command = svncommands.commandExportFile(revision, config.svnPath, fileInfo['svnPath'])
        results = svncommands.execute(command)
        if results:
            print(results)
    else:
        print("isn't archive")

if __name__ == "__main__":

    # файл в архиве без вложенных директорий
    # main("LLT_MC21_FCS_CU_BSP_LIB_ACE_3_UP_PJ21_PC004","ptu","r26651")

    # файл в архиве с вложенной директорией
    # main("mono-2.0-bdwgc","dll","r26542")

    # файл без архива 
    # main("robot","cpp","r26640")

    t = ['A    workspace\\LLT_MC21_FCS_CU_BSP_LIB_ACE_3_UP_PJ21_PC004.zip', 'Export complete.']
    r = t[0].split('    ')[-1].replace('\\','/')
    print(r)
    