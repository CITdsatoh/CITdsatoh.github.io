#encoding:utf-8

from PIL import Image,UnidentifiedImageError
from PIL.ExifTags import TAGS
import os
from datetime import datetime


#与えられたファイルからExif情報を取り出して、撮影日時を特定  
class IdentifyTakenDate:
   
   def __init__(self,img_path):
   
     self.__img_path=img_path
     self.__exif=None
     
     img_obj=None
     
     try:
      img_obj=Image.open(self.__img_path)
     #画像データが壊れている場合や正しく認識できなかった場合は、このエラーが出る。その時はとりあえず何もしない
     except UnidentifiedImageError:
       pass
       
     if img_obj is not None:
       try:
        self.__exif=img_obj._getexif()
       #exifが呼べなくてエラーになった場合に出る。この処理は後でするのでここではとりあえず何もしない
       except AttributeError:
         pass
     
   
   def get_real_taken_date(self):
      #画像データが壊れている、あるいは画像は正常だがexif情報がない場合は代わりに、更新日時か作成日時の古い方の日時を撮影日時とみなし,代替する
      if self.__exif is None:
        return self.get_provisonal_taken_time()
      
      exif_table=self.get_exif_table()
      
      #exifはあっても撮影日時がない場合は,それも更新日時か作成日時の古い方で代替
      if "DateTimeOriginal" not in exif_table:
        return self.get_provisonal_taken_time()
      
      #以下はexifも存在し、撮影日時も存在する場合.(年月日時分秒まで必要)
      date_time_str=exif_table["DateTimeOriginal"]
      date_time_list=date_time_str.split(" ")
      ymd=date_time_list[0].split(":")
      hms=date_time_list[1].split(":")
      
      t_year=int(ymd[0])
      t_month=int(ymd[1])
      t_date=int(ymd[2])
      t_hour=int(hms[0])
      t_minute=int(hms[1])
      t_second=int(hms[2])
      
      #返却はdatetime型にする
      date_on_datetime=datetime(year=t_year,month=t_month,day=t_date,hour=t_hour,minute=t_minute,second=t_second)
      
      return date_on_datetime
   
   def get_exif_table(self):
      exif_table={}
      for exif_id,exif_value in self.__exif.items():
         exif_name=TAGS.get(exif_id)
         exif_table[exif_name]=exif_value
      
      return exif_table     
     
   #exif情報が(png等)なかったり、exifがあっても撮影日時がない場合は、更新日時、作成日時の古い方で代替する
   def get_provisonal_taken_time(self):
      c_date_time_stamp=os.path.getctime(self.__img_path)
      m_date_time_stamp=os.path.getmtime(self.__img_path)
      
      older_time_stamp=m_date_time_stamp if m_date_time_stamp < c_date_time_stamp else c_date_time_stamp
      older_date=datetime.fromtimestamp(older_time_stamp)
      
      #返却はdatetime型そのまま
      
      return older_date
  
   def __str__(self):
     exif_info="file_path:"+self.__img_path+"\nextention:"+self.__img_path[self.__img_path.rindex(".")::]+"\n"
     is_exist_exif=False
     try:
       if self.__exif is not None:
         exif_table=self.get_exif_table()
         #exifそれ自体が存在しても内容がない場合は意味がないので、ここではexif_tableに内容がある場合のみを見る
         if exif_table:
           for exif_name,exif_value in exif_table.items():
              exif_name_str=exif_name+":"
              exif_value_str=f"{exif_value}"
              exif_one_info=exif_name_str+exif_value_str+"\n"
              exif_info += exif_one_info
           
           is_exist_exif=True
              
     except(UnidentifiedImageError,AttributeError,TypeError):
       pass
    
    
     if not is_exist_exif:
       date_info=self.get_provisonal_taken_time()
       date_data="%d:%d:%d"%(date_info.year,date_info.month,date_info.day)
       exif_info +="taken_date:"+date_data
         
     return exif_info
   
   @property
   def img_path(self):
     return self.__img_path
   
   @property
   def exif(self):
     return self.__exif
