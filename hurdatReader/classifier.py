#!/usr/bin/env python 3.2
'''
Module to classify storm type based on the Saffir-Simpson Scale.

Import and call methods.

@author: David Stack
'''

__all__ = ['classify', 'test']

def classify(wind):
    '''Classifies strom based on wind speed. Winds are in knots.'''
    if wind < 34:
        cat = 'TD'
    elif (34 <= wind and wind <= 63):
        cat = 'TS'
    elif (64 <= wind and wind <= 82):
        cat = 'H1'
    elif (83 <= wind and wind <= 95):
        cat = 'H2'
    elif (96 <= wind and wind <= 113):
        cat = 'H3'
    elif (114 <= wind and wind <= 135):
        cat = 'H4'
    elif wind > 135:
        cat = 'H5'
    return cat

def test():
    '''Test function.'''
    print('---Module classifier test---')

# Run test if module is run as a program
if __name__ == '__main__':
    test()
