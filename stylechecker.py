import os, subprocess

print('*** Running style checker on directory. ****')

path = os.getcwd()

dir = os.listdir(path)
for file in dir:
    if file[-3:] == '.py':
        subprocess.call(['pycodestyle', file])
