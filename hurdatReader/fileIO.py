#!/usr/bin/env python 3.2
'''
Module for reading and creating files on any OS.

Import and call methods.

@author: David Stack
'''

__all__ = ['openFile', 'makeTextFile', 'test']

import os

def openFile(filename, root=''):
    '''Opens file for read on Windows, Mac, and Linux.'''
    path = os.path.join(root, filename)
    hurdatData = open(path,'r')
    return hurdatData

def makeTextFile(filename):
    '''Opens new file for write.'''
    if os.path.isfile(filename):
        print(filename, 'already exists.')
        prompt = True
        while prompt == True:
            userInput = input('Overwrite (y/n)? ')
            if userInput == ('y' or 'Y'):
                f = open(filename,'w')
                prompt = False
            elif userInput == ('n' or 'N'):
                newFilename = input('Enter new filename: ')
                if not os.path.isfile(newFilename):
                    f = open(newFilename,'w')
                    prompt = False
                else:
                    print(newFilename, 'already exists.')
            else:
                print("Please enter either 'y' or 'n'.")
    else:
        f = open(filename,'w')
    return f

def test():
    '''Test function.'''
    print('---Module FileIO test---')

# Run test if module is run as a program
if __name__ == '__main__':
    test()
