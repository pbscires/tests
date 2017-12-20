#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: pranavburugula
"""

import wfdb
import os
import numpy as np
import pandas as pd
import re
import sys
from multiprocessing import Pool

mitDir = sys.argv[1]
print ("mitDir = ", mitDir)
os.chdir(mitDir)
channelsList = list(range(23))

filesList = os.listdir(mitDir)
print ('Number of files to be processed = {}'.format(len(filesList)))
# print (filesList)

epochLength = 1000 # In milliseconds
slidingWindowLength = 10 # In number of epochs

def calculateLineLength(filename):
    if (re.search('\.dat', filename) != None):
        fileBasename = os.path.splitext(filename)[0]
        print ("fileBasename = ", fileBasename)
        try:
            sig, fields = wfdb.srdsamp(fileBasename)
        except ValueError:
            print("ValueError occurred for fieBasename ", fileBasename)
            return
        print (fields['signame'])
#        return
        numChannels = len(fields['signame'])
        numSamples = fields['fs'] * 3600
        # fields['fs'] contains the frequency
        numSamplesPerEpoch = int(fields['fs'] * 1000 / epochLength)
        allChannelsDF = pd.DataFrame(data = sig[:,:], columns = fields['signame'])
        llDf = pd.DataFrame(columns = fields['signame'])
        print (allChannelsDF.shape)
#        for i in range(20):
#            allChannelsDF = allChannelsDF.add(other = sig[i, :])
        print (allChannelsDF.head())
        
        for i in range(1000):
            if (i > numSamplesPerEpoch):
                row = allChannelsDF.iloc[i-1] - allChannelsDF.iloc[i]
                for j in range(2, numSamplesPerEpoch):
                    row = row + (allChannelsDF.iloc[i-j] - allChannelsDF.iloc[i-j+1])
#                llDf = llDf.append(allChannelsDF.iloc[i] - allChannelsDF.iloc[i+1], 
#                                   ignore_index=True)
                llDf = llDf.append(row, ignore_index=True)
                
        print ("Printing Line Length Data frame")
        print (llDf.head())
    return


p = Pool()
#p.map(calculateLineLength, [filesList[0]])
print (filesList[0])
calculateLineLength(filesList[0])
