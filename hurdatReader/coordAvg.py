#!/usr/bin/env python 3.2
'''Module for averaging GPS coordinates together based on spherical shape
    of the Earth or summing the area found through integration.

Import and call methods.

@author: David Stack
'''

import math

__all__ = ['avgAll', 'avgMid', 'avgFirst', 'avgLast', 'calcScale',
           'weightedAvgCoords', 'test']

def __mean(nums):
    '''Calculates average of a list.'''
    if len(nums):
        return float( sum(nums) / len(nums))
    else:
        return 0.0

def __toCartesian(lat, lon):
    lat = math.radians(lat)
    lon = math.radians(lon)
    x = math.cos(lat) * math.cos(lon)
    y = math.cos(lat) * math.sin(lon)
    z = math.sin(lat)
    cartCoords = [x,y,z]
    return cartCoords

def __avgCoords(latList, lonList):
    '''Calculates cartesian coordinates from lat lon using geographic midpoint.
    Returns lat/lon coords in degrees.'''
    xList = []
    yList = []
    zList = []
    for i in range(0, len(lonList)):
        coords = __toCartesian(latList[i], lonList[i])
        xList.append(coords[0])
        yList.append(coords[1])
        zList.append(coords[2])
    x = __mean(xList)
    y = __mean(yList)
    z = __mean(zList)
    
    lon = math.atan2(y, x)
    hyp = math.sqrt(x * x + y * y)
    lat = math.atan2(z, hyp)
    lon = math.degrees(lon)
    lat = math.degrees(lat)
    coords = [lat, lon]
    return coords

def __calcDif(aList):
    '''Calculates difference between items in a list and returns a list of
    differences.'''
    difList = []
    for item in aList:
        if item == aList[0]:
            prevItem = item
        else:
            currentItem = item
            difList.append(math.fabs(currentItem - prevItem))
            prevItem = currentItem
    return difList
            
def calcScale(latList, lonList):
    '''Calculates scale of storm based on number of measurements.'''
    deltaLatList = __calcDif(latList)
    deltaLonList = __calcDif(lonList)
    scale = sum(deltaLatList) * sum(deltaLonList)
    return scale
    
def avgAll(latList, lonList):
    '''Averages all poins in list.  Method 1.'''
    average = __avgCoords(latList, lonList)
    return average

def avgMid(latList, lonList, windList, numMeas):
    '''Averages numMeas on either side of highest point in windList. Method 2.'''
    maxWind = max(windList)
    #print('Max Wind:',maxWind)
    mid = windList.index(maxWind)
    #print('Mid:', mid)
    if maxWind == windList[0]:
        #print('Special Case')
        average = __avgCoords(latList, lonList)
    elif mid-numMeas < 0:
        #print('Special Case 2')
        average = __avgCoords(latList[0:mid+numMeas],lonList[0:mid+numMeas])
    else:
        #print('Normal')
        average = __avgCoords(latList[mid-numMeas:mid+numMeas],lonList[mid-numMeas:mid+numMeas])
    return average

def avgFirst(latList, lonList, numMeas):
    '''First day (first numMeas measurements) average. Method 3.'''
    average = __avgCoords(latList[:numMeas], lonList[:numMeas])
    return average

def avgLast(latList, lonList, numMeas):
    '''Last day (last numMeas measurements) average. Method 4.'''
    average = __avgCoords(latList[-numMeas:], lonList[-numMeas:])
    return average

def __calcWeight(scale, scaleMax):
    '''Calculates weight of storm givin a list of corresponding scales.'''
    weight = scale / scaleMax
    return weight

def weightedAvgCoords(latList, lonList, scale, scaleMax):
    '''Determines weighted lat and lon by integrating over each
    and weighting by the provided weight for i number of storms. Returns a list
    of coordinates.'''
    weight = __calcWeight(scale, scaleMax)
    coords = __avgCoords(latList, lonList)
    lat = coords[0] * weight
    lon = coords[1] * weight
    weightedAvg = [lat, lon]
    return weightedAvg

def test():
    '''Test function.'''
    print('---Module coordAvg test---')

    latList = [28.0, 28.0, 28.0, 28.1, 28.2, 28.3, 28.4, 28.6, 29.0, 29.5, 30.0,
               30.5, 31.0]
    lonList = [94.8, 95.4, 96.0, 96.5, 97.0, 97.6, 98.3, 98.9, 99.4, 99.8, 100.0,
               100.1, 100.2]
    windList = [80, 80, 80, 80, 70, 60, 60, 50, 50, 40, 40, 40, 40]
    numMeas = 4
    #
    print('--Actual Values--')
    print('All  :', [28.904683, 97.985048])
    print('Mid  :', [])
    print('First:', [28.026472, 95.674809])
    print('Last :', [30.250083, 100.024174])
    print('--Test Values--')
    print('All  :', avgAll(latList, lonList))    
    print('Mid  :', avgMid(latList, lonList, windList, numMeas))    
    print('First:', avgFirst(latList, lonList, numMeas))    
    print('Last :', avgLast(latList, lonList, numMeas))

    print('\n***__mean Test***')
    meanList = [10, 20, 30]
    calcMean = __mean(meanList)
    if 20 != calcMean:
        print('!!!---TEST FAIL---!!!')
        print('Actual Mean:', 20)
        print('Calc Mean:',calcMean)
    else:
        print('PASS')
        
    print('\n***__toCartesian Test***')
    lat = 28.0
    lon = 94.8
    cart = __toCartesian(lat, lon)
    if [-0.07388315034589424, 0.8798509713754594, 0.4694715627858908] != cart:
        print('!!!---TEST FAIL---!!!')
        print('Actual Cart:', [-0.07388315034589424, 0.8798509713754594, 0.4694715627858908])
        print('Calc Cart  :', cart)
    else:
        print('PASS')

    print('\n***weightedAvgCoords Test***')
    latList = [25.6,26.8,28.1,29.3,30.2,31.3,32.9,35.1,37]
    lonList = [-61.2,-63,-64.6,-65.9,-65.8,-64,-60.9,-57.2,-53.5]
    scale = 194.94
    scaleMax = 1591.04
    test = weightedAvgCoords(latList, lonList, scale, scaleMax)
    test = [round(test[0],1),round(test[1],1)]
    known = [3.8,-7.6]
    if known != test:
        print('!!!---TEST FAIL---!!!')
        print('Actual:', known)
        print('Calc  :', test)
    else:
        print('PASS')

    print('\n***__calcDif Test***')
    aList = [25.6,26.8,28.1,29.3,30.2,31.3,32.9,35.1,37]
    test = __calcDif(aList)
    for i in range(0,len(test)):
        test[i] = round(test[i],4)
    known = [1.2,1.3,1.2,0.9,1.1,1.6,2.2,1.9]
    if known != test:
        print('!!!---TEST FAIL---!!!')
        print('Actual:', known)
        print('Calc  :', test)
    else:
        print('PASS')

    print('\n***__calcWeight Test***')
    scale = 194.94
    scaleMax = 1591.04
    test = round(__calcWeight(scale,scaleMax),6)
    known = 0.122524
    if known != test:
        print('!!!---TEST FAIL---!!!')
        print('Actual:', known)
        print('Calc  :', test)
    else:
        print('PASS')

    print('\n***calcScale Test***')
    latList = [25.6,26.8,28.1,29.3,30.2,31.3,32.9,35.1,37]
    lonList = [-61.2,-63,-64.6,-65.9,-65.8,-64,-60.9,-57.2,-53.5]
    test = round(calcScale(latList, lonList),2)
    known = 194.94
    if known != test:
        print('!!!---TEST FAIL---!!!')
        print('Actual:', known)
        print('Calc  :', test)
    else:
        print('PASS')
        
# Run test if module is run as a program
if __name__ == '__main__':
    test()
