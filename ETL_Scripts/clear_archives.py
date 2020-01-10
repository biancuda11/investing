import shutil
import os
import datetime as dt
from datetime import datetime
import os, time, sys

# purpose of this script is to clear any files in the archive older than 5 days

source = 'C:/Users/us52873/Documents/Personal/investing/data_files/archives/'

current_time = time.time()

print('current time ', current_time)

files = os.listdir(source)

files_removed = []

for f in files:

    f = source + f

    creation_time = os.path.getctime(f)

    time_since_creation = (current_time - creation_time) // (24*3600)

    if time_since_creation >= 3:
        os.unlink(f)
        print('{} removed'.format(f))
        files_removed.append(f)


if len(files_removed) > 0:
    print('Removed {} files'.format(len(files_removed)))
else:
    print('No Outdated Files \n')

print('DONE: Outdated Files Moved')
print('===========')
