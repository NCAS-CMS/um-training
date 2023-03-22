'''
   Useful subroutines for file conversions
'''


def dataFrameFromSpreadsheet(filename):
    ''' make pandas dataframe from a file '''
    import pandas as pd
    
    # only does .xlxs atm
    if filename.lower()[-5:] == '.xlsx':
        return pd.ExcelFile(filename).parse()
    else:
        raise ValueError('include other file types later')
