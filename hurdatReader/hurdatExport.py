#!/usr/bin/env python 3.2
'''
Module for exporting data from a HURDAT data file.

Reads a HURDAT data file and saves a text file with the following rows:
id, name, year, month, day, hour, lat, lon, windSpeed, pressure, stage,
category, landfall

Import and call methods.

@author: David Stack
'''

__all__ = ['exportToCSV', 'exportToTXT', 'test']

import os, fileIO
import hurdatReader as hr

def exportToCSV(hurdatData, filename):
    '''Loops through and saves HURDAT data as a csv file.'''
    csvExport = fileIO.makeTextFile(filename)
    csvExport.write('ID, name, year, month, day, hour, lat, lon, wind, pressure, stage, category, landfall')
    print('Saving file...')
    hourList = [0,6,12,18]
    for line in hurdatData:
        if hr.isHeader(line):
            ID = hr.getStormID(line)
            name = hr.getName(line).strip()
            year = hr.getYear(line)
            landfall = hr.madeLandfall(line)
        elif hr.isFooter(line):
            pass
        else:
            x = 11
            y = 28
            for i in range(4):
                lon = hr.getLon(line, x, y)
                if (hr.getLat(line, x, y) and lon != 0.0):
                    if lon >= 180.0:
                        lon = (lon - 360)*-1
                    else:
                        lon = lon * -1
                    csvExport.write('\n')
                    csvExport.write(str(ID))
                    csvExport.write(', ' + name)
                    csvExport.write(', ' + str(year))
                    csvExport.write(', ' + str(hr.getMonth(line)))
                    csvExport.write(', ' + str(hr.getDay(line)))
                    csvExport.write(', ' + str(hourList[i])) # write hour
                    csvExport.write(', ' + str(hr.getLat(line, x, y)))
                    csvExport.write(', ' + str(lon))
                    csvExport.write(', ' + str(hr.getWind(line, x, y)))
                    csvExport.write(', ' + str(hr.getPressure(line, x, y)))
                    csvExport.write(', ' + str(hr.getStage(line, x, y)))
                    csvExport.write(', ' + str(hr.getCategory(line, x, y)))
                    csvExport.write(', ' + str(landfall))
                x = y
                y = x + 17
                if hr.getMonth(line) == 12 and hr.getDay(line) == 31 and hourList[i] == 18:
                    year = year + 1                
    csvExport.close()
    print(csvExport.name, 'saved to', os.getcwd(), '\n')

def exportToTXT(hurdatData, filename):
    '''Loops through and saves HURDAT data as a txt file.'''
    txtExport = fileIO.makeTextFile(filename)
    txtExport.write('{0:6} {1:11}{2:4} {3:2} {4:2} {5:2} {6:6} {7:6} {8:2} {9:4} {10:16} {11} {12}'.format(
        'ID', 'name', 'year', 'mo', 'da', 'hr', 'lat', 'lon', 'wi', 'pre','stage', 'ct', 'landfall'))
    print('Saving file...')
    hourList = [0,6,12,18]
    for line in hurdatData:
        if hr.isHeader(line):
            ID = hr.getStormID(line)
            name = hr.getName(line)
            year = hr.getYear(line)
            landfall = hr.madeLandfall(line)
        elif hr.isFooter(line):
            pass
        else:
            x = 11
            y = 28
            for i in range(4):
                if (hr.getLat(line, x, y) and hr.getLon(line, x, y)) != 0.0:
                    txtExport.write('\n')
                    txtExport.write('{0} {1}{2} {3:2d} {4:2d} {5:2d} {6:5.1f} {7:6.1f} {8:3d} {9:4d} {10:16} {11} {12}'.format(
                        ID, name, year,
                        hr.getMonth(line), hr.getDay(line), hourList[i],
                        hr.getLat(line,x,y), hr.getLon(line,x,y),
                        hr.getWind(line,x,y), hr.getPressure(line,x,y),
                        hr.getStage(line,x,y), hr.getCategory(line,x,y),
                        landfall))
                    #txtExport.write(' ' + str(hr.madeLandfall(line)))
                x = y
                y = x + 17
                if hr.getMonth(line) == 12 and hr.getDay(line) == 31 and hourList[i] == 18:
                    year = year + 1
    txtExport.close()
    print(txtExport.name, 'saved to', os.getcwd(), '\n')

def test():
    '''Test function.'''
    print('---Module hurdatExport test---')

# Run test if module is run as a program
if __name__ == '__main__':
    test()
