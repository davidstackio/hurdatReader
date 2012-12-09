#!/usr/bin/env python 3.2
'''
Main file to run HURDAT analysis.

@author: David Stack
'''

import hurdatExport, fileIO, coordExport

# Read HURDAT Data
print('-----')
print('Reading HURDAT data...')
print('-----')
hurdatData = fileIO.openFile('HURDAT_tracks1851to2010_atl_2011rev.txt', '..\\data')
hurdatExport.exportToCSV(hurdatData, '..\\output\\HURDAT_Export.csv')
hurdatData.seek(0, 0)
hurdatExport.exportToTXT(hurdatData, '..\\output\\HURDAT_Export.txt')
hurdatData.close()

# Average coordinates with all observations
print('-----')
print('Saving average coordinates data...')
print('-----')
hurdatExportFile = fileIO.openFile('..\\output\\HURDAT_Export.txt')
coordExport.exportToTXT(hurdatExportFile, '..\\output\\Coord_Export.txt')

# Average coordinates using filters
# Only category TS-H5 Storms
hurdatExportFile.seek(0, 0)
filterTerms = {'cat':['TS','H1','H2','H3','H4','H5']}
coordExport.exportToTXT(hurdatExportFile, '..\\output\\Coord_Export_TS-H5.txt', filterTerms)
# Only storms that made landfall
hurdatExportFile.seek(0, 0)
filterTerms = {'landfall':1}
coordExport.exportToTXT(hurdatExportFile, '..\\output\\Coord_Export_Landfall.txt', filterTerms)
# Only storms that made landfall and were category H3-H5
hurdatExportFile.seek(0, 0)
filterTerms = {'landfall':1,'cat':['H3','H4','H5']}
coordExport.exportToTXT(hurdatExportFile, '..\\output\\Coord_Export_Landfall_H3-H5.txt', filterTerms)
hurdatExportFile.close()

print('-----')
print('All files successfully created.')
print('-----')
