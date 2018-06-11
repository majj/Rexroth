# -*- coding: utf-8 -*-

"""
simulator for FTP file creation.


"""

import os
import glob
import time


def move_old_file():
        
    data_files = glob.glob("data/*.json")
    
    for data_file in data_files:
        statinfo = os.stat(data_file)
        
        if time.time() - statinfo.st_atime  > 60:
            os.remove(data_file)
            print("delete %s" % (data_file))
            
            
    pass
    


def main():
    
    print (time.ctime())

    with open('torque.data', 'r') as fh:
        
        data = fh.read()
        
        
        while True:
            #print(data)            
            
            filename = time.strftime("SP06_P10_%y%m%d%H%M%S.Json",time.localtime())
            
            #create json file in ./data
            with open(os.sep.join(["data",filename]), 'w') as fh_o:
                fh_o.write(data)
                
            move_old_file()
            
            time.sleep(15)
            
            
        
if __name__ == '__main__':

    main()


    