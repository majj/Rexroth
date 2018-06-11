# -*- coding: utf-8 -*-

"""
simulator for FTP file creation.
"""

import os
import glob
import time


def move_old_file(base_path):
    
    file_path = os.sep.join([base_path,"*.json"])
    
    data_files = glob.glob(file_path)
        
    
    for data_file in data_files:
        statinfo = os.stat(data_file)
        
        if time.time() - statinfo.st_atime  > 60:
            try:
                os.remove(data_file)
                print("delete %s" % (data_file))
            except:
                print("failed to remove")
                pass

def main():
    
    base_path = "..\\data"
    
    print (time.ctime())

    with open('torque.data', 'r') as fh:
        
        data = fh.read()        
        
        while True:
            #print(data)            
            
            filename = time.strftime("SP06_P10_%y%m%d%H%M%S.Json",time.localtime())
            
            #create json file in ./data
            with open(os.sep.join([base_path,filename]), 'w') as fh_o:
                fh_o.write(data)
                print("new %s" % (filename))
                
            move_old_file(base_path)
            
            time.sleep(15)
            
            
if __name__ == '__main__':

    main()


    