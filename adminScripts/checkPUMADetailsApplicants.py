'''
   Python 2 code to check status of applicants to training courses on PUMA
   Run as python [this script.py] [applicant list . txt]
   Location: puma:/home/dcase/pythonScripts/trainingScripts
'''

import sys

# details of accounts on PUMA
passwordFile = '/etc/passwd'

# Read in names of applicants
with open(sys.argv[1], 'r') as infile:
    applicantNames = infile.read().split('\n')

# Remove tabs (if copied from spreadsheet)
applicantNames = map(lambda x: x.replace('\t', ' '), applicantNames)
print applicantNames

def bogusName(testName):
    #remove any wierd ones / buggy things
    if testName == '':
        return True
    return False

def pumaName(testName, detailsFile):
    ''' Look in detailsFile for the name '''
    with open(detailsFile, 'r') as df:
        for line in df.readlines():
            if testName.replace(' ', '').lower() in line.replace(' ', '').lower():
                return line.split(':')[0]


# Try to find names on system
print 'PUMA account'
for name in applicantNames:
    if bogusName(name):
        continue
    pn = pumaName(name, passwordFile)
    if pn:
        print pn
    else:
        print ''
