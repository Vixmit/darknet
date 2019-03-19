import sys
import glob
import os
 
index = 0
 
for file in list(glob.glob('/home/tomasz/Desktop/test_good/*')):
    print(index)
    print(file + "    ")
    os.system("python test.py "+ file )
    index += 1
