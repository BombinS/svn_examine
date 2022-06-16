import fixScadeCsv

def getCsvSingleLineInfo(path, target):
    class Single:
        def __init__(self):
            self.counter = 0
        def increment(self):
            self.counter += 1
            return self.counter
        def checkcell(self):
            return(logging.warning("you'v bad values for #Phase cell"))

    import pandas as pd
    import logging
    logging.basicConfig(filename='getCsvSingleLineInfo.log',level=logging.WARNING)
    cnt=Single()
    outs = 'error'
    badvalues=["#Phase","Phase"]
    target1="#Phase:"
    if target=="phase":
        try:
            df = pd.read_csv(path,sep=';',header=None, engine='python')
        except Exception as e:
            maxNumberOfColumns = int(e.args[0].split()[-1])
            fixScadeCsv.fixScadeCsv(path, maxNumberOfColumns)
            try:
                df = pd.read_csv(path,sep=';',header=None, engine='python')
            except:
                print(path,' ', e)
                return
        r=df.shape[0]
        c=df.shape[1]
        for i in range(r):
            for j in range(c):
                s=df.iloc[i,j]
                if (s==target1):
                    sing=cnt.increment()
                    ssing=str(sing)
                    if sing>1 :
                        logging.warning(" %s'#Phase:' raised an error",  ssing)
                    outs=df.iloc[i,j+1]; 
                    if "".__eq__(outs):
                        logging.warning("you'v empty value for #Phase")   
                        
                elif (s in badvalues):
                    cnt.checkcell()
                else:
                    continue
    return outs

if __name__ == "__main__":
    path='workspace/MC21_SWA_M_FWS_CHOICE.csv'
    target="phase"
    print(getCsvSingleLineInfo(path, target))
