#!/usr/bin/env python 3.2
'''Module for exporting averaged GPS coordinates to a text file.

Import and call methods.

@author: David Stack
'''

import os, fileIO, coordAvg

__all__ = ['exportToTXT', 'getScaleList', 'test']

scaleList = []

def getScaleList():
    '''Returns scaleList for use with weighted averaging.'''
    return scaleList

def __getID(line):
    if line == '':
        ID = -999
    else:
        ID = line[0:6]
    return ID

def __getName(line):
    name = line[7:17]
    return name

def __getYear(line):
    year = line[18:22]
    return year

def __getMonth(line):
    month = line[23:25]
    return month

def __getDay(line):
    day = line[26:28]
    return day

def __getHour(line):
    hour = line[29:31]
    return hour

def __getLat(line):
    lat = float(line[32:37])
    return lat

def __getLon(line):
    lon = float(line[38:44])
    return lon

def __getWind(line):
    wind = int(line[45:48])
    return wind

def __getPres(line):
    pres = int(line[49:53])
    return pres
        
def __getStage(line):
    stage = line[54:70]
    return stage

def __getCat(line):
    cat = line[71:73]
    return cat

def __getLandfall(line):
    landfall = int(line[74])
    return landfall

def __filterData(dataFile, filterTerms, searchType='and'):
    '''Filters data based on filterTerms and optional searchType ('and' or 'or').

    These filterTerms can include 'stage', 'cat', and 'landfall' and must be in the
    dictionary format ({key:value}). For 'stage' and 'cat' multiple entries can be entered
    as a list. 'landfall' must be entered as an integer. The searchType can either be 'and' or 'or'.'''
    newData = []
    dataFile.readline() # Reads headers
    
    for line in dataFile:
        addCat = True
        addLandfall = True
        addStage = True
        if 'stage' in filterTerms:
            stageList = filterTerms['stage']
            if __getStage(line).strip() not in stageList:
                addStage = False
        if 'cat' in filterTerms:
            catList = filterTerms['cat']
            if __getCat(line).strip() not in catList:
                addCat = False
        if 'landfall' in filterTerms:
            landfall = filterTerms['landfall']
            if __getLandfall(line) != landfall:
                addLandfall = False
        if searchType == 'and':
            if addStage and addCat and addLandfall:
                newData.append(line)
        else:
            if addStage or addCat or addLandfall:
                newData.append(line)
    return newData

def exportToTXT(hurdatExport, filename, filterTerms={}, numMeas=4):
    '''Loops through hurdatExport.txt and saves relevent averages.

    Optionally choose number of measurements used (default = 4).
	Optionally filter data file.  See __filterData() for more info.
    Creates file with headers: ID,decade,startYear,startMonth,startDay,
    startHour,name,avgAll,avgMid,avgFirst,avgLast.'''
    hurdatExport.readline() # Reads headers
    txtExport = fileIO.makeTextFile(filename)
    txtExport.write('ID     dec  year mo dy hr name       allLat     allLon     midLat     midLon     firstLat   firstLon   lastLat    lastLon')
    print('Saving file...')

    if filterTerms == {}:
        lineList = hurdatExport.readlines()
    else:
        lineList = __filterData(hurdatExport,filterTerms)
    lineList.append('')
    for i in range(len(lineList)):
        nextLine = lineList[i]
        if i == 0:
            prevID = 'null'
            line = nextLine
            continue
        ID = __getID(line)
        nextID = __getID(nextLine)
        if ID != prevID:
            #print(ID)
            latList = []
            lonList = []
            windList = []
            prevID = ID
            name = __getName(line)
            startYear = __getYear(line)
            decade = startYear[0:3] + '0'
            startMonth = __getMonth(line)
            startDay = __getDay(line)
            startHour = __getHour(line)
            # landfall =

        # store avg lat, lon, and wind
        #print('Storing info...')
        lat = __getLat(line)
        lon = __getLon(line)
        wind = __getWind(line)
        latList.append(lat)
        lonList.append(lon)
        windList.append(wind)
        
        if ID != nextID:
            #print('Writing...')
            txtExport.write('\n')
            avgAll = coordAvg.avgAll(latList, lonList)
            avgMid = coordAvg.avgMid(latList, lonList, windList, numMeas)
            #print('WindList:',windList)
            avgFirst = coordAvg.avgFirst(latList, lonList, numMeas)
            avgLast = coordAvg.avgLast(latList, lonList, numMeas)
            scale = coordAvg.calcScale(latList, lonList)
            scaleList.append(scale)
            txtExport.write('{0} {1} {2} {3} {4} {5} {6} {7:10.6f} {8:10.6f} {9:10.6f} {10:10.6f} {11:10.6f} {12:10.6f} {13:10.6f} {14:10.6f}'.format(ID,decade,startYear,startMonth,startDay,startHour,name,
			avgAll[0],-avgAll[1],avgMid[0],-avgMid[1],avgFirst[0],-avgFirst[1],avgLast[0],-avgLast[1]))
            write = False
        prevID = ID
        line = nextLine
    print(txtExport.name, 'saved to', os.getcwd(), '\n')

def test():
    '''Test function.'''
    print('---Module coordExport test---')

    hurdatExport = fileIO.openFile('HURDAT_Export.txt')
    hurdatExport.readline() # Reads headers
    line = hurdatExport.readline()
    
    print('***__getStage test***')
    print('Stage   :',__getStage(line))

    print('***__getCat test***')
    print('Cat     :',__getCat(line))

    print('***__getLandfall test***')
    print('Landfall:',__getLandfall(line))

    print('***__filter test***')
    filterTerms = {}
    #filterTerms = {'cat':['TS','H1','H2','H3','H4','H5']}
    filterTerms = {'stage':'Tropical Cyclone'}
    searchType = 'and'
    filteredData = __filterData(hurdatExport, filterTerms, searchType)
    verbose = False
    if verbose:
        for line in filteredData:
            print(line)
    print('Number of entires found:',len(filteredData))

# Run test if module is run as a program
if __name__ == '__main__':
    test()
