import logging
import os
import dbcommands
import svncommands
import config
import ScadeMatrixParser

target = 'SWA'

def main(target):
    f = open('{}_scade.csv'.format(target), 'a')

    #init logging
    logging.basicConfig(filename='fill_scade_phase.log', encoding='utf-8', level=logging.DEBUG)    
    
    #init database connection 
    dbcommands.initDb(config.dbserver, config.db)
    
    #prepare work directory
    if not os.path.isdir('./workspace'):
        os.makedirs('./workspace')

    DistinctCsvScadeFilenames = dbcommands.getDistinctScadeFileNames(target, 'csv')

    for DistinctCsvScadeFilename in DistinctCsvScadeFilenames:
        LastScadeFilenameInfo = dbcommands.getLastScadeFilenameInfo(target, 'csv', DistinctCsvScadeFilename)
        command = svncommands.commandIsFileExistAtLastRevison(DistinctCsvScadeFilename, 'csv', LastScadeFilenameInfo[1], config.svnPath)
        svnCommandResult = svncommands.execute(command)
        if svnCommandResult:
            command = svncommands.commandExportArchive(LastScadeFilenameInfo[0], config.svnPath, LastScadeFilenameInfo[1], DistinctCsvScadeFilename, 'csv')
            svncommands.execute(command)
            try:
                phase = ScadeMatrixParser.getCsvSingleLineInfo('workspace/{}.csv'.format(DistinctCsvScadeFilename), 'phase')
            except:
                print("exception on {}".format(DistinctCsvScadeFilename))
            line = "{};{};{};{};".format(DistinctCsvScadeFilename, phase, LastScadeFilenameInfo[3], LastScadeFilenameInfo[2])
            f.write(line + '\n')

    f.close()

if __name__ == '__main__':
    main(target)