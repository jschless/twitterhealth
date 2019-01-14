'''
trains a neural network dataset according to engineered features
'''
import pandas as pd
import phemeParser


pathToPheme = 'C:\\Users\\EECS\\Documents'

threadList = phemeParser.parsePheme(pathToPheme)
print(threadList)
