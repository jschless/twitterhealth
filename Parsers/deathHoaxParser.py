''' for compiling list of tweets into one large dataset to be hydrated'''

import os
import sys

path = 'C:\\Users\\EECS\\Documents\\DeathHoax\death-hoaxes-dataset.tar\death-hoaxes-dataset\death-hoaxes-dataset'

deathMap = {}
listOfIds = []
for dirName in os.listdir(path): #each person folder
    for lastFolder in os.listdir(path + '\\' + dirName):
        file = open(path + '\\' + dirName + '\\' + lastFolder + '\\tweets.dat')
        for line in file:
            listOfIds.append(line)
print(len(listOfIds))
#with open('toHydrate.txt', 'w+') as outfile:
#    outfile.write("\n".join(listOfIds))

#450*(24*4)
