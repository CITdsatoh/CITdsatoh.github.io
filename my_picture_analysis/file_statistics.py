#encoding:utf-8
import os
from file_counter import FileCountersByDate
from datetime import datetime
from file_statistics_util import MONTH_DAYS,is_correct_date,is_leap_month,is_leap_year
from identify_date import IdentifyTakenDate

class FileStatistics:
   
   
   def __init__(self,files):
     self.__files=files
     self.__files_by_hours=[0 for i in range(24)]
     self.__size_by_hours=[0 for i in range(24)]
     self.__days_files=[0,0,0,0,0,0,0]
     self.__days_size=[0,0,0,0,0,0,0]
     self.__files_by_dates=FileCountersByDate()
     self.__arrange()
   
   def __arrange(self):
      for one_file in self.__files:
        file_date_getter=IdentifyTakenDate(one_file)
        file_date_info_datetime=file_date_getter.get_real_taken_date()
        hour=file_date_info_datetime.hour
        day=file_date_info_datetime.weekday()
        size=os.path.getsize(one_file)
        self.__files_by_dates.count(file_date_info_datetime.year,file_date_info_datetime.month,file_date_info_datetime.day,size)
        self.__days_files[day] +=1
        self.__days_size[day]+=size
        self.__files_by_hours[hour] +=1
        self.__size_by_hours[hour]+=size
   
   def get_information_on_date(self,one,two=None,three=None,type="number"):
     
     #最後の引数が与えられないとき
     if three is None:
     
       #1つしか引数が与えられなかったとき
       if two is None:
       
         #仮にその引数が13から99の間の場合,現在21世紀なので,先頭の20が省略されたと考えて,引数に2000を足した都市のファイルの数を調べる
         if 13 <= one and one <= 99:
            one += 2000
            
         #修正後も含めその1つの引数が4桁の数字だった時は,年だけが与えられたと考えるため、その年のファイルの数、あるいはファイルの大きさの合計を調べる
         if len(str(one)) == 4:
            return self.__files_by_dates.query_files_information(type,year=one)
         #その1つの引数が1から12の間だった時は、月だけが与えられたと考えるため、その月のファイルの数、あるいはファイルの大きさの合計を調べる
         if 1 <= one and one <= 12:
            return self.__files_by_dates.query_files_information(type,month=one)
         
      
       #2つ引数が与えられたき
       else:
          #1つ目の引数(one)が13から99の間で、2つ目の引数(two)が、1から12の数字だった場合は、西暦の先頭の20が省略された年と月が与えられていると考える
          if 13 <= one and one <= 99 and 1 <= two and two <= 12:
             one += 2000
             
          #1つ目の引数(one)が4桁の数字で、2つ目の引数(two)が、1から12の数字だった場合は、年と月が与えられていると考える
          if len(str(one)) == 4 and 1 <= two and two <= 12:
            return self.__files_by_dates.query_files_information(type,year=one,month=two)
            
          #それ以外の場合、1つ目は月、2つ目は日が与えられていると考える
          #正しい日付指定かどうか調べて、日付として存在すれば処理を行う
          if is_correct_date(one,two):
              return self.__files_by_dates.query_files_information(type,month=one,date=two)
              
          #それ以外は指定ミスと考え、0を返す
          return 0
             
     
     #以下はきちんと3つ引数が与えられた場合（年・月・日がすべて与えられた場合)
     
     #最初の引数(年)が13から99の場合、西暦の先頭の20が省略されたと考えるため,2000を足しておく.
     if 13 <= one and one <= 99: 
        one += 2000
        
     #最後に日付指定がおかしくないかを確認
     if is_correct_date(two,three):
         return self.__files_by_dates.query_files_information(type,year=one,month=two,date=three)
     
     
     return 0
     
   def get_exists_file_day_rate(self,one,two=None):
   
     #開始年の開始月・終了年の終了月への対応(開始年が1月1日から活動していると限らないこと、開始月が1日から活動していると限らないこと）から処理する必要がある
     #終了年・終了月も同様。（終了年が12月31日まで活動していると限らないこと、終了月が,最終日(30日・31日・28（29）日)までやっているとかぎらない
     period=self.get_start_goal_years()
     start_year=period["start"]["year"]
     goal_year=period["goal"]["year"]
     start_month=period["start"]["month"]
     goal_month=period["goal"]["month"]
     start_date=period["start"]["date"]
     goal_date=period["goal"]["date"]
     
     #1つしか引数が与えらなかったとき
     if two is None:
     
       #2桁の数字13~99が与えられたら、それは、西暦の先頭の20が省略されたとみなし,2000を足して年だけ与えられた時と同じ処理をする
       if 13 <= one and one <= 99:
         one += 2000
       
       year_long=366 if is_leap_year(one) else 365
       
        
       #修正も含めて4桁の数字1つが引数として与えられたら、それは年が与えられたとみなし、その年の活動日数（ファイルが1枚でも存在する日）を返す
       if len(str(one)) == 4:
       
         #この与えられた引数が,もし仮に活動を開始した年だった場合,その年は1月1日からきちんと活動しているとは限らないので
         #逆にこの引数が、活動を終了した年と同じだった場合、その年は12月31日まできちんと活動しているとは限らないので
         if one == start_year:
           start_month_days=MONTH_DAYS[start_month] if is_leap_month(start_year,start_month) else 29
           year_long=(start_month_days-start_date)+1
           for one_month in range(start_month+1,12+1):
              one_month_days=MONTH_DAYS[one_month] if is_leap_month(start_year,one_month) else 29
              year_long += one_month_days
         
         if one == goal_year:
           year_long=0
           for one_month in range(1,goal_month):
              one_month_days=MONTH_DAYS[one_month] if is_leap_month(start_year,one_month) else 29
              year_long += one_month_days
           year_long += goal_date
         
              
          
         file_exists_days=self.__files_by_dates.get_file_exist_days(year=one)
         rate=file_exists_days/year_long
         return (year_long,file_exists_days,rate)
       
       #1から12の間の2桁の数字が1つ与えられた時は,それは月（年によらないもの）だと考える
       if 1 <= one and one <= 12:
       
           #まずは,年によらないその月の長さを得て、活動日数を得る
           one_month_long=MONTH_DAYS[one]
           file_exists_days=self.__files_by_dates.get_file_exist_days(month=one)
           
           #次に活動していた期間中に、その月が何回やってきたかを求める
           
           
           #活動期間中にその月がやってきた回数
           years_time=(goal_year-start_year)+1
           
           #ただし、与えられた月が、活動を始めた年の活動を始めた月より前なら、最初の年の与えられた月時点ではまだ活動していないということだから除く
           #また、活動を始めた月そのものについても、1日からきちんと活動しているとは限らないので、ここでは取り除く（以下で個別対応）
           if one <= start_month:
              years_time -= 1
           #逆に、与えられた月が、活動を終えた年の活動を終えた月より後なら、その年のその月時点ではもう活動していないということだからこれものぞく
           #また、活動を終える前の最後の月そのものについても、最終日(28（29）日・30日・31日)まで活動しているとも限らないので、取り除く（以下で個別対応)
           if goal_month <= one:
              years_time -=1
           
           
           #活動期間中の与えられた月の日数の合計(月の日数*その月がやってきた回数)
           all_days=one_month_long*years_time
           
           #活動を始めた年の最初の月への対応
           if one == start_month:
              start_month_days=MONTH_DAYS[one]-start_date+1
              all_days += start_month_days
           
           if one == goal_month:
              all_days += goal_date
           
           #うるう日への対応
           if one == 2:
              #仮に1月で活動を終了した場合,2月は含まれないので、yearのカウントから取り除く(もし仮にそのままカウントすると、うるう日計算が狂うため)
              if one == 1:
                 goal_year -= 1
              
              #期間中のうるう年の回数
              leap_years_num=len([year for year in range(start_year,goal_year+1) if is_leap_year(year)])
              
              #うるう年の回数=うるう日の日数なので、そのままうるう年の数を足せばよい
              all_days += leap_years_num
           
           rate=file_exists_days/all_days
           
           
           return (all_days,file_exists_days,rate)
       
       #それ以外は変な年(16384年とか西暦2年とか）が与えられたとみなす。(ファイルと活動率は0を返す)
       return (year_long,0,0.0)
       
     
     
     #以下は、2つ引数が与えられた時（月日については活動率を求める必要がない（その日に活動があれば100%,していなければ0ということが自明なので）
     #ゆえに、2つ引数が与えられた場合は年・月が与えられているものだとみなす
     
     #第二引数(月)がきちんと,1~12月までの月が与えられたなら
     if 1 <= two and two <= 12:
     
        month_days=MONTH_DAYS[two] if not is_leap_month(one,two) else 29
        
        #第一引数（年）が0~99の間だった場合は西暦の先頭の20が抜けていると判断
        if 0 <= one and one <= 99:
           one += 2000
           
        #修正も含めて、きちんと西暦が4桁の数字であれば
        if len(str(one)) == 4:
          
          if one == start_year and two == start_month:
             month_days=(month_days-start_date)+1
          
          if one == goal_year and two == goal_month:
             month_days=goal_date
             
          file_exists_days=self.__files_by_dates.get_file_exist_days(year=one,month=two)
          rate=file_exists_days/month_days
          return (month_days,file_exists_days,rate)
        
        return(month_days,0,0.0)
     
     #13月等月の指定が不正なら、
     return (0,0,0.0)
        
   
   def get_exists_file_weekdays_rate(self):        
      return self.__files_by_dates.get_file_exists_weekdays_on_period()
         
   def get_file_numbers_information(self,one,two=None,three=None):
      return  self.get_information_on_date(one,two,three,"number")
   
   def get_file_size_information(self,one,two=None,three=None):
      return  self.get_information_on_date(one,two,three,"size")         
   
   def get_start_goal_years(self):
      return self.__files_by_dates.get_periods_years()
   
      
  
   @property
   def files(self):
      return self.__files
   
   @property
   def days_files(self):
      return self.__days_files
   
   @property
   def days_size(self):
      return self.__days_size
   
   @property
   def files_by_hours(self):
      return self.__files_by_hours
   
   @property
   def size_by_hours(self):
       return self.__size_by_hours
   
   

    