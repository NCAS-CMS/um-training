''' 
python3 (DHC used anaconda)
takes spreadsheet (consider whitespace) and makes neater document
Does this for NCAS-CMS tutorials, to get data on applicants    
AT THE MOMENT CHANGE fileName TO BE FILE OF INTEREST and just run python [this].py [filename]
'''

import numpy as np
import pandas as pd
import sys

# Choose whether to make pdf and/or html outputs
makingHTMLFiles = False
makingPDFs = True
if len(sys.argv) > 2:
    pdf_output_file = sys.argv[2]
else:
    pdf_output_file = 'Applicants.pdf'

if makingPDFs:
    try:
        import pdfkit
    except:
        #proceed with no pdf output
        makingPDFs = False
        ImportError('No pdfkit - use pip or conda e.g. conda install -c conda-forge python-pdfkit')


# could use sys.argv[1] or something, but need name to be readable by python
fileName = sys.argv[1]#'sensiblyNamed.xlsx'

# choose to split all applicants onto separate pages in .pdf
pdfPageBreak = True

#Standard strings to go around body (can link to .css later)
htmlHeadString = '''<!DOCTYPE html>
<html>
<head>
<title>Page Title</title>

    <style>
      .content {
      font-style: normal;
      font-size: 18px;
      padding-top: 4.0em;
      margin-left: 2.5em;
      margin-right: 2.5em;
      }
    </style>

</head>
<body>
<div class="content">
'''

htmlFootString = '''</div>
</body>
</html>'''
htmlPageBreak  = '<p style="page-break-after: always">\n'

def dropDownGenerator(dataList):
    ''' dataList maps human readable names to URL (filename)
        list because maintain order
        Inserts (into body) dropdown menu '''
    
    return '''<form name="dropdown">
<select onchange="location = this.options[this.selectedIndex].value;">
  <option>Applicants</option>
'''+\
'\n'.join(['  <option value="applicant{}.html">{}</option>'.format(str(x[0]), x[1]) for x in dataList]) + '''
</select> 
</form>
'''

def dataFrameFromFile(filename):
    ''' make pandas dataframe from a file '''

    # only does .xlxs atm
    if filename.lower()[-5:] == '.xlsx':
        return pd.ExcelFile(filename).parse()
    else:
        raise ValueError('include other file types later')

def bestMatchFromRow(row, headerName, strictCount=False):
    ''' In cases wherein two rows have same headerName (postgrad/researcher) (!!!) 
        find non-empty/None match '''

    _headers = np.array(list(row.iteritems()))[:,0] #must be a method for this
    if strictCount:
        _maxColumnSameNames = len([x for x in _headers if headerName == x])
    else:
        _maxColumnSameNames = len([x for x in _headers if headerName in x])

    if _maxColumnSameNames == 1:
        return row[headerName]

    bestValue = ''
    # Assume that name convention is to keep adding numbers- return 1st string found
    if isinstance(row[headerName], str):
        bestValue = max([bestValue, row[headerName]])
    else:
        for i in map(str, range(1, _maxColumnSameNames)):
            if isinstance(row[headerName + '.' + i], str):
                bestValue = max([bestValue, row[headerName + '.' + i]])
#                return    row[headerName + '.' + i]

    return bestValue #this will do, as they may not have entered anything
#    raise Exception('Lazy exception bestMatchFromRow ' + headerName)
    
def pageFromDataFrameRow(dfRow):
    ''' html page to match Annette's eg from each row of DataFrame 
        Where names of columns change, an attempt is made to find the index '''

    #outString is in html format- can be body of document (lacks header etc)
    outString  = '<h1> {} {}</h1>\n'.format(dfRow['First Name'], dfRow['Last Name'])
    outString += '<p> {}</p>\n'.format(dfRow['Email Address'])
    outString += '<p> {} {} Funding: {}</p>\n'.format(dfRow['Application Type'],
                                                      dfRow['Year of Study'],
                                                      bestMatchFromRow(dfRow, 'Funding Body'))
    outString += '<p> {} {}</p>\n'.format(bestMatchFromRow(dfRow, 'University/Institution'),
                                          bestMatchFromRow(dfRow, 'Department'))
    
    # some headers are substrings-- but risk substrings not unique
    bestSupervisorName = max([x for x in [bestMatchFromRow(dfRow, 'Supervisor Name', strictCount=True),
                                          bestMatchFromRow(dfRow, 'PI/Supervisor Name', strictCount=True),
                                          ''] if isinstance(x, str)])
    outString += '<p> Supervisor: {}</p>\n'.format(bestSupervisorName)

    outString += '<h2>Title: {}</h2>\n'.format(bestMatchFromRow(dfRow, 'Project Title'))
    outString += '<p>{}</p>\n'.format(bestMatchFromRow(dfRow, 'Research Description (maximum 1000 characters)'))
    outString += '<p>{} {}</p>\n'.format(bestMatchFromRow(dfRow, 'Employer'),
                                         bestMatchFromRow(dfRow, 'Role Title'))
    outString += '<p>{}</p>\n'.format(bestMatchFromRow(dfRow, 'Role Description'))
    outString += '<h2>UM configuration</h2>\n'
    _indexUMConfColumn = np.where(dfRow.keys().str.contains('UM config', na=False))[0][0]
    outString += '<p>{}</p>\n'.format(dfRow[_indexUMConfColumn])
    outString += '<p>Machine: {}</p>\n'.format(dfRow['Machine'])
    outString += '<h2>Supporting statement</h2>\n'
    outString += '<p>{}</p>\n'.format(dfRow['Supporting Statement (maximum 1000 characters)'])
    
    #remove all nan with whitespace (ignore inelegance)
    return outString.replace('nan', '')

df = dataFrameFromFile(fileName)
#assert(all([x in df.loc[0].keys() for x in needed keys]))

#sort df if want to
df = df.sort_values('Last Name')

# Use dropdown list in html - nameList holds this info
nameList = [[index, row['First Name'] + ' ' + row['Last Name']] for index, row in df.iterrows()]

# Remove Dave Case (dont want him round these parts)
#df = df[df.Last_Name != 'Case'] #space in index is a pain!!
#df = df.drop(df.index[8])

# You can make html files for each applicant, with a dropdown to jump between them
if makingHTMLFiles:
    # Change file names to people names if needed (rm whitespace)
    for index, row in df.iterrows():
        with open('applicant{}.html'.format(index), 'w') as outf:        
            outf.write(htmlHeadString +\
                       dropDownGenerator(nameList) +\
                       pageFromDataFrameRow(row) +\
                       htmlFootString)

# No dropdown in pdf
if makingPDFs:
    if pdfPageBreak:
        exampleString = '\n'.join([htmlHeadString +\
                                   pageFromDataFrameRow(row) +\
                                   htmlPageBreak +\
                                   htmlFootString for index, row in df.iterrows()])
    else:
        exampleString = '\n'.join([htmlHeadString +\
                                   pageFromDataFrameRow(row) +\
                                   htmlFootString for index, row in df.iterrows()])
    pdfkit.from_string(exampleString, pdf_output_file)
