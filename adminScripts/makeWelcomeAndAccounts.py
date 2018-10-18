'''
   Make document which contains attendees details/passwords and info
   Python 3 (conda should have dependencies, except pdfkit)
'''

import os
import pdfkit
import pandas as pd
from jinja2 import Template
from customFileReading import dataFrameFromSpreadsheet

#global (independent of attendee) values
inputFilename  = 'ApplicantSummary.xlsx'
outputFilename = 'welcomeAndAccounts.pdf'
htmlBase       = 'welcomeAndAccounts.html'
# assume htmlBase and images are kept in same dir as this script
htmlBase = os.path.dirname(os.path.realpath(__file__)) + '/' + htmlBase
staticDir = os.path.dirname(os.path.realpath(__file__)) + '/'
courseDates    = '7-9 November 2018'
courseLocation = 'PC Room G10, Allen Lab, University of Reading'

template    = Template(open(htmlBase, 'r').read())

# Insert page-breaks
htmlPageBreak  = '<p style="page-break-after: always">\n'

#Read .xlsx file with candidate info
df = dataFrameFromSpreadsheet(inputFilename)

exampleString = '\n'.join([template.render(attendeeName   = row['First Name'] +\
                                                            ' ' +\
                                                            row['Last Name'],
                                           staticDir      = staticDir,
                                           uorUsername    = row['ITS account'],
                                           pumaUsername   = row['PUMA account'],
                                           mosrsUsername  = row['MOSRS account'],
                                           archerUsername = row['ARCHER account'],
                                           courseLocation = courseLocation,
                                           courseDates    = courseDates) +\
                           htmlPageBreak for index, row in df.iterrows()])
#print(exampleString)
pdfkit.from_string(exampleString, outputFilename)
