#encoding:utf-8

import os
import pathlib
import glob
import re
from datetime import datetime
from result_writer import ResultWriter




def get_files_path():
   all_files=glob.glob("*/**/*",recursive=True)
   return [one_file for one_file in all_files if re.search("\\.(jpg|jpeg|png|gif|bmp|tif|tiff)$",one_file,re.IGNORECASE)]



def main():
  
  files=get_files_path()
  writer=ResultWriter(files,os.getcwd())
  writer.result_write(True)
  writer.result_write(False)
  writer.f_write_by_weekdays_and_hour()
  
  
  

if __name__ == "__main__": 
     
     main()    
        
         
           
        
      
       