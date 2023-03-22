'''
   Python 2 - check whether helpdesk created
   Read some IDs and check whether they are in a particular file
   Run as python [this script.py] [applicant list . txt]
   Prints Need Puma if PUMA account not given, Y/N whether this account has a helpdesk
   Location: /var/trac/ncascms/temp/trainingScripts
   on ncascms@man.badc.rl.ac.uk
'''
import sys

# details of accounts
detailsFile = '/var/trac/ncascms/trac_env/conf/passwd'

# Read in IDs of applicants
with open(sys.argv[1], 'r') as infile:
    applicantIDs = infile.read().split('\n')

#print applicantIDs;exit()
    
def idAppears(testID, infoFile):
    ''' Is id in infoFile? -> Y/N '''
    with open(infoFile, 'r') as df:
        for line in df.readlines():
            if testID == line.split(':')[0]:
                return 'Y'
    return 'N'

for aID in applicantIDs:
    if aID == '':
        print 'Need PUMA'
    else:
        print idAppears(aID, detailsFile)
