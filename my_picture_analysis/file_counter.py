#encoding:utf-8

from file_statistics_util import MONTH_DAYS,is_leap_month,is_leap_year,get_goal_date,get_days_between_two_dates
from datetime import datetime



class FileCountersByDate:
   
   
   def __init__(self):
     #ここには各年・月・日のファイル数あるいはファイルサイズデータを入れる
     self.__date_dict={}
     
     #年関係なく、月・日のみのファイル数あるいはファイルサイズデータを入れる
     self.__non_year_date_dict={}
   
   def count(self,year,month,date,size):
      
      if year not in self.__date_dict.keys():
        self.__date_dict[year]={}
        #"sum"というキーにはその年の合計(numberキーはファイル数、sizeキーは合計サイズを格納、daysは1年のうち何日分ファイルがあるか（写真をとったか）を格納)
        #さしあたり,Noneを入れておき、初めて以下の枚数・サイズ計算メソッドが呼ばれたときに合計を計算。
        #2回目以降は,計算を複数回わざわざしないようにこのキーの値を返すようにする
        self.__date_dict[year]["sum"]={}
        self.__date_dict[year]["sum"]["number"]=None
        self.__date_dict[year]["sum"]["size"]=None
        self.__date_dict[year]["sum"]["days"]=None
        
      if month not in self.__date_dict[year].keys():
        self.__date_dict[year][month]={}
        #"sum"というキーにはその年・月の合計(numberキーはファイル数、sizeキーは合計サイズを格納,daysは1か月のうち何日間写真を撮ったかを格納)
         
        self.__date_dict[year][month]["sum"]={}
        self.__date_dict[year][month]["sum"]["number"]=None
        self.__date_dict[year][month]["sum"]["size"]=None
        self.__date_dict[year][month]["sum"]["days"]=None
      
      if month not in self.__non_year_date_dict.keys():
        self.__non_year_date_dict[month]={}
        self.__non_year_date_dict[month]["sum"]={}
        self.__non_year_date_dict[month]["sum"]["number"]=None
        self.__non_year_date_dict[month]["sum"]["size"]=None
        self.__non_year_date_dict[month]["sum"]["days"]=None
        
      
      #以下は活動日数は必要ない
       
      if date not in self.__date_dict[year][month].keys():
        self.__date_dict[year][month][date]={}
        self.__date_dict[year][month][date]["number"]=1
        self.__date_dict[year][month][date]["size"]=size
        
      else:
        self.__date_dict[year][month][date]["number"] += 1
        self.__date_dict[year][month][date]["size"]+=size
      
      if date not in self.__non_year_date_dict[month].keys():
        self.__non_year_date_dict[month][date]={}
        self.__non_year_date_dict[month][date]["number"]=1
        self.__non_year_date_dict[month][date]["size"]=size
      else:
        self.__non_year_date_dict[month][date]["number"] += 1
        self.__non_year_date_dict[month][date]["size"]+=size
      
    
   #枚数・サイズ計算
   def query_files_information(self,type,year=None,month=None,date=None):
       count=0
       years=self.get_years()
       
       #月日は関係なく、その年のファイルの数(大きさ)を計算する時（2018年1年間の間に作成されたファイル数の合計、あるいはファイルの大きさの合計,2019年1年間の間に作成されたファイルの数あるいは,ファイルの大きさの合計を調べるなど・・)
       if year is not None and month is None and date is None:
       
         #そもそも、yearキーが辞書に存在しない場合,その年のファイルは1枚もないので0を返す
         if year not in self.__date_dict.keys():
           return 0
          
       
         #ここから、もし,sumというキー（ここには1年間の合計枚数・合計サイズを格納しておく）が,これがNoneならまだ合計が計算されていないということだから計算
         if self.__date_dict[year]["sum"][type] is None:
           for one_month in range(1,12+1):
             end_day=MONTH_DAYS[one_month] if not is_leap_month(year,one_month) else 29
             for one_date in range(1,end_day+1):
                try:
                 count += self.__date_dict[year][one_month][one_date][type]
                #keyErrorはキーの登録がない時、つまり、上に記述された日付に作成されたファイルが1つも存在しないがゆえに、キーとして登録されなかったために出現するエラーである。
                #なので、このエラーが出たときはその日付のファイルが1つもないということだから何もしなくてよい
                except KeyError:
                 pass       
                  
           self.__date_dict[year]["sum"][type]=count
           return count
           
           
         return self.__date_dict[year]["sum"][type]
         
       #ある特定の年月のファイルの数を計算する時（例えば、2018年7月に作成されたファイルの数あるいはファイルの大きさの合計を計算するなど）
       if year is not None and month is not None and date is None:
         
          #ただし,ファイルが1つもない月はmonthのキーが作られないので、計算の対象外
          if year not in self.__date_dict.keys() or month not in self.__date_dict[year].keys():
             return 0
        
          
          #sumキーには、その年の月の合計枚数（サイズ）が格納されるが、このメソッドが呼ばれるのが1回目の場合、まだNoneが入ったままである.
          #その時は改めて計算する  
          if self.__date_dict[year][month]["sum"][type] is None:
            end_day=MONTH_DAYS[month] if not is_leap_month(year,month) else 29
            for one_date in range(1,end_day+1):     
              try:
                count += self.__date_dict[year][month][one_date][type]
              except KeyError:
                pass
                
            self.__date_dict[year][month]["sum"][type]=count
            return count
          
          
          return self.__date_dict[year][month]["sum"][type]
            
          
       #ある特定の1日のファイルの数を計算する時(例えば、2019年1月1日に作成されたファイルの数あるいはファイルの大きさの合計を計算する時）
       #year,month,dateがすべて指定されているとき
       if year is not None and month is not None and date is not None:
          try:
            return self.__date_dict[year][month][date][type]
          #このエラーが出た日付のファイルはないということだから0を返す
          except KeyError:
            return 0
          
       
       #年によらず月だけの枚数を検索（年に関係なく1月に作成されたファイルの数、2月（2018年、2019年、2020年関係なく2月という月）に作られたファイルの数あるいはファイルの大きさの合計etc)
       if year is None and month is not None and date is None:
         #写真が1枚も存在しない月は、そもそもmonthのキー自体が作成されないので、その時は0を返す.まずはmonthがキーとしてあるか調べる
         if month not in self.__non_year_date_dict.keys():
            return 0
       
         if self.__non_year_date_dict[month]["sum"][type] is None:
           for one_year in years:
             end=MONTH_DAYS[month] if not is_leap_month(one_year,month) else 29
             for one_date in range(1,end+1):
                if month in self.__date_dict[one_year] and one_date in self.__date_dict[one_year][month]:
                   try:
                    count += self.__date_dict[one_year][month][one_date][type]
              
                    #このエラーが出るということはその時のファイルは0枚ということだから何もしない(countに加算しない)
                   except KeyError:
                     pass
                   
           self.__non_year_date_dict[month]["sum"][type]=count         
           return count
        
         
         return self.__non_year_date_dict[month]["sum"][type]
          
       
       #年によらず、月日の枚数（年によらず1月1日のファイルの数、あるいはファイルの大きさの合計、年によらず1月2日のファイルの数あるいはファイルの大きさの合計etc)
       if year is None and month is not None and date is not None:
          try:
            return self.__non_year_date_dict[month][date][type]
            
          #その月日のファイルが1つもないとエラーが出るため0を返す
          except KeyError:
            return 0
       
       #その他、変な日付が入れられたりパターン指定がおかしかったりする場合は0を返す
       return 0
   
   
    
   def get_years(self):
       return sorted(list(self.__date_dict.keys()))
         
   #最古のファイルと最新のファイルの作成日時を得る
   def get_periods_years(self):
       #昇順ソート済みの年が入っている
       year_period=self.get_years()
       #一番古いファイルが作成された年は、当然0番目に入っている
       start_year=year_period[0]
        
       #以降は,{年(数字):{月1:{日付1:{"number":枚数,"size":合計サイズ},日付2:{{"number":枚数,"size":合計サイズ}},},月2:{日付1:{}..}}}という構造であるため,
       #一番古い年の中から一番古い月を得るためには,一番古い年のディクショナリからキー(キーが月の数字となっているため)だけを取り出して、ソートして0番目の要素を取り出せばよい
       #ここでソートをするのはディクショナリは順番を保障しないためである。
       #そして、このキーには月名の数字の他に、sumという文字列が入っているので取り除かなければならない
       month_period=sorted([month_num for month_num in self.__date_dict[start_year].keys() if type(month_num) == int])
       start_month=month_period[0]
        
       #日付も同様で,一番古い年の一番古い月のディクショナリからキーを取り出し、ソートして0番目の要素を取り出せばよい
       date_period=sorted([date_num for date_num in self.__date_dict[start_year][start_month].keys() if type(date_num) == int])
       start_date=date_period[0]
        
       #逆に一番新しい日付は,一番最後の要素を取り出せばよい
       #考え方は上と同様
       goal_year=year_period[len(year_period)-1]
       #goal_month_period=sorted(list(self.__date_dict[goal_year].keys()))
       goal_month_period=sorted([month_num for month_num in self.__date_dict[goal_year].keys() if type(month_num) == int])
       goal_month=goal_month_period[len(goal_month_period)-1]
       #goal_date_period=sorted(list(self.__date_dict[goal_year][goal_month].keys()))
       goal_date_period=sorted([date_num for date_num in self.__date_dict[goal_year][goal_month].keys() if type(date_num) == int])
       goal_date=goal_date_period[len(goal_date_period)-1]
        
       return {"start":{"year":start_year,"month":start_month,"date":start_date},"goal":{"year":goal_year,"month":goal_month,"date":goal_date}}
       
   #1年、あるいは1か月、あるいは特定の月にファイルが存在する日が何日間あるかを調べるメソッド
   def get_file_exist_days(self,year=None,month=None,date=None):
      
      count=0
      #特定の1年の活動日数(1枚でもファイルがある日)を計算
      if year is not None and month is None and date is None:
        #そもそも引数として与えられたyearがキーとして存在しない場合は、ファイル自体がないということだから
        if year not in self.__date_dict.keys():
           return 0
           
        if self.__date_dict[year]["sum"]["days"] is None:
           for now_month in range(1,12+1):
              end_day=MONTH_DAYS[now_month] if not is_leap_month(year,now_month) else 29
              for now_date in range(1,end_day+1):
                 if now_month in self.__date_dict[year].keys() and now_date in self.__date_dict[year][now_month].keys():
                     count += 1
           
           self.__date_dict[year]["sum"]["days"]=count
           return count
        
        return  self.__date_dict[year]["sum"]["days"]
      
      #特定の年月（2018年1月など）の活動日数（1枚でもファイルがある日)を計算
      if year is not None  and month is not None and date is None:
        
        if year not in self.__date_dict.keys() or month not in self.__date_dict[year][month].keys():
            return 0
        
        if self.__date_dict[year][month]["sum"]["days"] is None:
           end_day=MONTH_DAYS[month] if not is_leap_month(year,month) else 29
           for now_date in range(1,end_day+1):
              if now_date in self.__date_dict[year][month].keys():
                 count +=1
           
           self.__date_dict[year][month]["sum"]["days"]=count
           
           return count
            
         
        return self.__date_dict[year][month]["days"]
      
      #年によらず特定の月(1月という月,2月という月など)の活動日数を計算
      if year is None and month is not None and date is None:
         
         if month not in self.__non_year_date_dict.keys():
            return 0
            
         if self.__non_year_date_dict[month]["sum"]["days"] is None:
           for now_year in self.get_years():
              end_day=MONTH_DAYS[month] if not is_leap_month(now_year,month) else 29
              for now_date in range(1,end_day+1):
                if now_date in self.__non_year_date_dict[month].keys():
                  count += 1
              
           self.__non_year_date_dict[month]["sum"]["days"]=count
           return count
         
         return self.__non_year_date_dict[month]["sum"]["days"]
       
      #日付エラーなどがあった場合
      return 0
       
   def get_file_exists_weekdays_on_period(self,start:dict=None,goal:dict=None):
      period=self.get_periods_years()
      if start is None:
        start=period["start"]
      if goal is None:
        goal=period["goal"]
      
      file_exists_weekdays_num=[0 for i in range(7)]
      pair=[]
      start_year=start["year"]
      goal_year=goal["year"]
      start_month=start["month"]
      start_date=start["date"]
      for now_year in range(start_year,goal_year+1):
         if now_year in self.__date_dict.keys():
             goal_month=goal["month"] if now_year == goal_year else 12
             for now_month in range(start_month,goal_month+1):
                 if now_month in self.__date_dict[now_year].keys():
                   goal_date=get_goal_date(goal_year,now_year,goal["month"],now_month,goal["date"])
                   for now_date in range(start_date,goal_date+1):
                      if now_date in self.__date_dict[now_year][now_month].keys():
                          weekday=datetime(year=now_year,month=now_month,day=now_date).weekday()
                          file_exists_weekdays_num[weekday] += 1
                   
                 start_date=1
                   
         start_month=1
         start_date=1
      
      #ファイルがある曜日を調べた後、次にこの区間が何日あるか調べる
      days_between_start_goal=get_days_between_two_dates(start,goal)
      
      #その後、開始日と終了日の曜日を調べる(曜日は数値型で0が月曜、1が火曜、6が日曜）
      goal_weekday=datetime(year=goal_year,month=goal["month"],day=goal["date"]).weekday()
      start_weekday=datetime(year=start_year,month=start_month,day=start_date).weekday()
      
      #開始日と終了日の間にそれぞれの曜日が何日間あるかを調べる(さしあたり7で割った商を採用)
      default_each_weekday_num=int(days_between_start_goal/7)
      
      #開始日と終了日のうち、早い方の曜日（月曜日に近い曜日）と遅い方の曜日（日曜日に近い曜日）を調べる
      #この間にある曜日は、他の曜日と比べて曜日数が1日多くなるので以下で別途処理する必要がある
      former_weekday=min(start_weekday,goal_weekday)
      later_weekday=max(start_weekday,goal_weekday)
      
      for weekday_number in range(7):
        real_weekday_num=default_each_weekday_num
        #さきほど上記で求めた曜日の間の曜日は1日多くなるのでここで1を足す
        if former_weekday <= weekday_number and weekday_number <= later_weekday:
           real_weekday_num += 1
        
        weekdays_pair={}
        weekdays_pair["all"]=real_weekday_num
        weekdays_pair["file_exists"]=file_exists_weekdays_num[weekday_number]
        pair.append(weekdays_pair)
     
      return pair
   
   def get_file_exist_days_in_period(self,start:dict=None,goal:dict=None):
     period=self.get_periods_years
     if start is None:
       start=period["start"]
     if goal is None:
       goal=period["goal"]
     
     days_between_start_goal=get_days_between_two_dates(start,goal)
     file_exists_days=0
     start_year=start["year"]
     start_month=start["month"]
     start_date=start["date"]
     goal_year=goal["year"]
     for now_year in range(start_year,goal_year+1):
        goal_month=goal["month"] if now_year == goal_year else 12
        for now_month in range(start_month,goal_month+1):
          goal_date=get_goal_date(goal_year,now_year,now_month,goal["month"],goal["date"])
          for now_date in range(start_date,goal_date+1):
            if is_file_exists_on_one_date(now_year,now_month,now_date):
                file_exists_days += 1
          
          start_date=1
          
        start_month=1
     
     return (days_between,file_exists_days)
       
        
   
   def is_file_exists_on_one_date(self,year=None,month=None,date=None):
     
      if year is not None:
      
        if year not in self.__date_dict.keys():
          return False 
          
        if month is not None and month not in self.__date_dict[year].keys():
          return False
        
        if date is not None and date not in self.__date_dict[year][month].keys():
          return False
        
        return True
      
      
      if month not in self.__non_year_date_dict.keys():
         return False
      
      if date is not None and date in self.__non_year_date_dict.keys():
         return False
      
      return True
      
    
        
        
          
        
        
    
       