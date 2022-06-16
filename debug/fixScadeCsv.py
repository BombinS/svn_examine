
def fixScadeCsv(path, maxNumberOFColumns):
    with open (path, 'r') as f:
        data = f.readlines()

    firstLine = data[0]
    firstLine = firstLine[:-1]
    while (firstLine.count(';') < maxNumberOFColumns - 1):
        firstLine += ';'
    firstLine += '\n'

    data[0] = firstLine

    with open (path, 'w') as f:
        f.writelines(data)    
    
if __name__ == '__main__':
    path = 'workspace/MC21_FWA_LOC_RESET_300.csv'
    fixScadeCsv(path)