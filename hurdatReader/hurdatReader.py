#!/usr/bin/env python 3.2
'''
Module for reading a HURDAT data file.

Import and call methods.

@author: David Stack
'''

__all__ = ['isHeader', 'isFooter', 'madeLandfall', 'getName', 'getYear',
           'getMonth', 'getDay', 'getStormNum', 'getNumDays', 'getDailyData',
           'getStage','getLat', 'getLon', 'getWind', 'getPressure',
           'getCategory','test']

import classifier

def isHeader(line):
    '''Returns True if line is header, false if not.'''
    if line[17:19] == 'M=':
        result = True
    else:
        result = False
    return result

def isFooter(line):
    '''Returns True if line is footer, false if not.'''
    result = False
    try:
        int(line[6])
    except ValueError:
        result = True
    return result

def madeLandfall(line):
    '''Returns if storm made landfall or not.'''
    if (isHeader(line) and line[52] == '1'):
        result = 1
    else:
        result = 0
    return result

def getName(line):
    '''Returns storm name.'''
    if isHeader(line):
        name = line[35:46]
    return name

def getYear(line):
    '''Returns storm year.'''
    if isHeader(line):
        year = line[12:16]
    return int(year)

def getMonth(line):
    '''Returns storm month.'''
    month = line[6:8]
    if month[0] == '0':
        month = ' ' + month[1]
    return int(month)

def getDay(line):
    '''Returns storm day.'''
    day = line[9:11]
    if day[0] == '0':
        day = ' ' + day[1]
    return int(day)

def getStormID(line):
    '''Returns the number of the storm (from total record).'''
    if isHeader(line):
        stormID = line[22:24].strip().zfill(2)
    stormID = str(getYear(line)) + stormID
    return int(stormID)

def getNumDays(line):
    '''Returns the number of days of data there are.'''
    if isHeader(line):
        numDays = int(line[19:21])
    return numDays

def getStage(line, x, y):
    subLine = line[x:y]
    stage = subLine[0]
    if stage == '*':
        stage = 'Tropical Cyclone'
    elif stage == 'S':
        stage = 'Subtropical'
    elif stage == 'E':
        stage = 'Extratropical'
    elif stage == 'W':
        stage = 'Wave'
    elif stage == 'L':
        stage = 'Remnant Low'
    return stage

def getLat(line, x, y):
    '''Returns the latitude for specific 6 hour measurement.'''
    subLine = line[x:y]
    lat = subLine[1:4]
    lat = lat[0:2] + '.' + lat[2]
    return float(lat)

def getLon(line, x, y):
    '''Returns the longitude for specific 6 hour measurement.'''
    subLine = line[x:y]
    lon = subLine[4:8]
    lon = lon[0:3] + '.' + lon[3]
    return float(lon)

def getWind(line, x, y):
    '''Returns wind spead for specific 6 hour measurement.'''
    subLine = line[x:y]
    wind = subLine[9:12]
    return int(wind)

def getPressure(line, x, y):
    '''Returns pressure for specific 6 hour measurement.'''
    subLine = line[x:y]
    pressure = subLine[13:17]
    if pressure == '   0':
        pressure = -999
    return int(pressure)

def getCategory(line, x, y):
    '''Returns category for specific 6 hour measurement.'''
    category = classifier.classify(getWind(line, x, y))
    return category

def test():
    '''Test function.'''
    print('---Module hurdatReader test---')
    import os, fileIO
    hurdatData = fileIO.openFile('HURDAT_tracks1851to2010_atl_2011rev.txt', '..\\data')
    hourList = [0,6,12,18]
    for line in hurdatData:
        if isHeader(line):
            ID = getStormID(line)
            name = getName(line).strip()
            year = getYear(line)
            landfall = madeLandfall(line)
        elif isFooter(line):
            pass
        else:
            x = 11
            y = 28
            for i in range(4):
                lon = getLon(line, x, y)
                if (getLat(line, x, y) and lon != 0.0 and year == 1886):
                    if lon >= 180.0:
                        lon = (lon - 360)*-1
                    else:
                        lon = lon * -1
                    print('\n')
                    print('ID   :', str(ID))
                    print('Name :', name)
                    print('Year :', str(year))
                    print('Month:', str(getMonth(line)))
                    print('Day  :', str(getDay(line)))
                    print('Hour :', str(hourList[i])) # write hour
                    print('Lat  :', str(getLat(line, x, y)))
                    print('Lon  :', str(lon).strip())
                    print('Wind :', str(getWind(line, x, y)))
                    print('Press:', str(getPressure(line, x, y)))
                    print('Stage:', getStage(line, x, y))
                    print('Cat  :', getCategory(line, x, y))
                    print('Land :', str(landfall))
                x = y
                y = x + 17
                if getMonth(line) == 12 and getDay(line) == 31 and hourList[i] == 18:
                    year = year + 1
    hurdatData.close()

# Run test if module is run as a program
if __name__ == '__main__':
    test()
