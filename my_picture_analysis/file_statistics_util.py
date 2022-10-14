#encoding:utf-8

from datetime import datetime
import pathlib
import os


MONTH_DAYS=(0,31,28,31,30,31,30,31,31,30,31,30,31)

dir_border_char="\\" if os.name == "nt" else "/"

#日付が正しいか（日付として存在するか）を調べるメソッド
#ここでは年は無視し、2月29日は正しい扱いとする
def is_correct_date(month,date):
   if month < 1 or 12 < month:
     return False
    
   end_day=MONTH_DAYS[month] if month != 2 else 29
   return 1 <= month and month <= end_day

#ここでは、年も考慮して日付として存在するかを調べる
#うるう年ではない2月29日は間違い扱い
def is_correct_one_day(year,month,date):
  if month < 1 or 12 < month:
     return False
  end_day=MONTH_DAYS[month] if is_leap_month(year,month) else 29
  return 1 <= month and month <= 12
  
#閏月（うるう年の2月）かどうかを調べる
def is_leap_month(year,month):
   if month != 2:
      return False
      
   return is_leap_year(year)
      
      
#うるう年かどうか             
def is_leap_year(year):
   return year % 4 == 0 and  year % 100 != 0 or year % 400 == 0


def get_goal_date(goal_year,now_year,goal_month,now_month,goal_date):
    
    if (goal_year == now_year) and (goal_month == now_month):
       return goal_date
    
    if is_leap_month(now_year,now_month):
       return 29
    
    return MONTH_DAYS[now_month]
   

def size_by_unit(size_byte_num):
   base_10=1
   digit=0
   while base_10 <= size_byte_num:
      digit +=1
      base_10 *= 10
   
   units=("B","KB","MB","GB","TB")
   units_ind=int((digit-1)/3)
   #絶対にないが,もし仮にファイルサイズの合計15桁以上になった場合,このunitsタプルには,PB（ペタ),EB(エクサ）がないため、エラーになってしまう。
   #ここではペタ・エクサは用いないものとし、テラ以上はすべて「テラ」で表すこととする
   if 15 <= digit:
      units_ind=4
      
   units_float=size_byte_num/(10**(units_ind*3))
   units_float_str="%.3f"%(units_float)
   return units_float_str+units[units_ind]

#与えられた2日間の日付の日数を返す
def get_days_between_two_dates(start:dict,goal:dict):

   goal_datetime=datetime(year=goal["year"],month=goal["month"],day=goal["date"])
   start_datetime=datetime(year=start["year"],month=start["month"],day=start["date"])
    
   #このままdatetime型同士で引き算してもまだtimedelta型なので,そこからdaysフィールドにアクセスし、絶対値計算
   days_timedelta=goal_datetime-start_datetime
   days_between_start_goal=abs(days_timedelta.days)
   
   return days_between_start_goal
   

def mk_save_dirs(c_dir,*sub_dirs):
   
   dir_string=c_dir
   for one_sub_dir in sub_dirs:
     dir_string += (dir_border_char+one_sub_dir)
     path_obj=pathlib.Path(dir_string)
     if not path_obj.exists():
        path_obj.mkdir()
        
   
   return dir_string
   

      

       