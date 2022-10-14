#encoding:utf-8

from file_statistics_util import MONTH_DAYS,is_leap_month,get_goal_date,size_by_unit,mk_save_dirs,dir_border_char
from file_statistics import FileStatistics
from data_manage import  DataByDate
import os

WEEKDAYS_NAME=["月","火","水","木","金","土","日"]

class ResultWriter:

   def __init__(self,files,save_dir=None):
     self.__files=files
     
     self.__save_parent_dir=save_dir
     if save_dir is None:
      self.__save_parent_dir=os.getcwd()
     
     self.__file_data_by_year=[]
     self.__file_data_by_y_month=[]
     self.__file_data_by_y_m_date=[]
     self.__file_data_by_only_month=[]
     self.__file_data_by_only_m_date=[]
     
     self.__no_files_days={}
     
     
     self.__f_analyser=FileStatistics(files)
     analyse_period=self.__f_analyser.get_start_goal_years()
     self.__start_date=analyse_period["start"]
     self.__goal_date=analyse_period["goal"]
     self.__date_arrange()
   
   
   def __date_arrange(self):
      start_year=self.__start_date["year"]
      goal_year=self.__goal_date["year"]
      start_month=self.__start_date["month"]
      start_date=self.__start_date["date"]
      
      #まずは「年だけ」、「年・月」、「年・月・日」のデータを集めて、
      for now_year in range(start_year,goal_year+1):
      
        year_f_num=self.__f_analyser.get_file_numbers_information(now_year)
        
        if year_f_num != 0:
          year_f_size=self.__f_analyser.get_file_size_information(now_year)
          year_f_rate=self.__f_analyser.get_exists_file_day_rate(now_year)
          
          year_manager=DataByDate([now_year,None,None],year_f_num,year_f_size,year_f_rate)
          self.__file_data_by_year.append(year_manager)
          
          goal_month=self.__goal_date["month"] if now_year == goal_year else 12
          
          for now_month in range(start_month,goal_month+1):
            y_month_f_num=self.__f_analyser.get_file_numbers_information(now_year,now_month)
            if y_month_f_num != 0:
              y_month_f_size=self.__f_analyser.get_file_size_information(now_year,now_month)
              y_month_f_rate=self.__f_analyser.get_exists_file_day_rate(now_year,now_month)
              y_month_manager=DataByDate([now_year,now_month,None],y_month_f_num,y_month_f_size,y_month_f_rate)
              self.__file_data_by_y_month.append(y_month_manager)
              
              goal_date=get_goal_date(goal_year,now_year,self.__goal_date["month"],now_month,self.__goal_date["date"])
              
              for now_date in range(start_date,goal_date):
                 y_m_date_f_num=self.__f_analyser.get_file_numbers_information(now_year,now_month,now_date)
                 if y_m_date_f_num != 0:
                   y_m_date_f_size=self.__f_analyser.get_file_size_information(now_year,now_month,now_date)
                   y_m_date_manager=DataByDate([now_year,now_month,now_date],y_m_date_f_num,y_m_date_f_size)
                   self.__file_data_by_y_m_date.append(y_m_date_manager)
                   
            start_date=1
        
        start_date=1
        start_month=1
        
      #次は年によらない「月・日」（1月1日だけ、1月2日だけのデータ）と「月」（年によらない8月分のデータなど）
      for now_month in range(1,12+1):
        month_f_num=self.__f_analyser.get_file_numbers_information(now_month)
        if month_f_num  != 0:
          month_f_size=self.__f_analyser.get_file_size_information(now_month)
          month_f_rate=self.__f_analyser.get_exists_file_day_rate(now_month)
          
          month_manager=DataByDate([None,now_month,None],month_f_num,month_f_size,month_f_rate)
          self.__file_data_by_only_month.append(month_manager)
          
          goal_day=MONTH_DAYS[now_month] if now_month != 2 else 29
          
          for now_date in range(1,goal_day+1):
            m_date_f_num=self.__f_analyser.get_file_numbers_information(now_month,now_date)
            
            #もし、その日付（年関係なく）のファイルが1つもなければ、別の無活動日リスト(ファイルが1つもない月日を入れておく)に入れておく
            if m_date_f_num == 0:
              month_str="%d月"%(now_month)
              date_str="%d日"%(now_date)
              if month_str not in self.__no_files_days.keys():
                self.__no_files_days[month_str]=[]
              
              self.__no_files_days[month_str].append(month_str+date_str)
              continue
              
              
            m_date_f_size=self.__f_analyser.get_file_size_information(now_month,now_date)
            m_date_manager=DataByDate([None,now_month,now_date],m_date_f_num,m_date_f_size)
            self.__file_data_by_only_m_date.append(m_date_manager)
          
         
   def result_write(self,year_write:bool):
   
     #第一引数:今回ファイルに書き込む対象のデータ 第二引数:保存先ディレクトリ(タプル) 第三引数:ファイル名の一部(共通部分） 第四引数 :上書きか、直書きか 第五引数:内容 第五引数：ソートするか否か
     #まずは「年別」のデータと「年・月別（2018年1月、2018年2月等）」のデータをファイル化
     
     if year_write:
       self.__fwrite(tuple(self.__file_data_by_year),("year_month","non_sort"),"photo_analyse_result_by_year_and_ymonth_not_sorted","w","年別",False)
       self.__fwrite(tuple(self.__file_data_by_y_month),("year_month","non_sort"),"photo_analyse_result_by_year_and_year_month_not_sorted","a","年・月別",False)
       self.__fwrite(tuple(self.__file_data_by_year),("year_month","sort"),"photo_analyse_result_by_year_and_year_month_sorted_by_","w","年別",True)
       self.__fwrite(tuple(self.__file_data_by_y_month),("year_month","sort"),"photo_analyse_result_by_year_and_year_month_sorted_by_","a","年・月別",True)
    
       #次に各「年・月・日」1日分のデータのファイル化
       self.__fwrite(tuple(self.__file_data_by_y_m_date),("year_month","date","non_sort"),"photo_analyse_result_by_year_month_date_not_sorted","w","年・月・日別",False)
       self.__fwrite(tuple(self.__file_data_by_y_m_date),("year_month","date","sort"),"photo_analyse_result_by_year_month_date_sorted_by_","w","年・月・日別",True)
       
       return 
     
     #年に関係ないバージョン
     if not year_write:
       self.__fwrite(tuple(self.__file_data_by_only_month),("non_year_month","non_sort"),"photo_analayse_result_by_month_and_mdate_regardless_year_not_sorted","w","月別",False)
       self.__fwrite(tuple(self.__file_data_by_only_m_date),("non_year_month","non_sort"),"photo_analayse_result_by_month_and_mdate_regardless_year_not_sorted","a","月・日別",False)
       
       #年に関係ないバージョンをソートする際は少し他の項目と処理を変えるので、別メソッドで対応
       #年に関係ないバージョンは、それぞれの年ごとの内訳も印字するためである
       self.__fwrite_special(tuple(self.__file_data_by_only_month),tuple(self.__file_data_by_y_month),("non_year_month","sort"),"photo_analayse_result_by_month_and_m_date_regardless_year_sorted_by_","w","月別")
       self.__fwrite_special(tuple(self.__file_data_by_only_m_date),tuple(self.__file_data_by_y_m_date),("non_year_month","sort"),"photo_analayse_result_by_month_and_m_date_regardless_year_sorted_by_","a","月・日別")
       
       #無活動日（活動した期間中のいずれの年も活動がなかった日付を表示
       self.__fwrite_no_files_days()
       
     
     
   def __fwrite(self,write_data:tuple,save_p_dirs:tuple,file_name_part:str,mode:str,content:str,is_need_sort:bool):
     
     is_need_rate=write_data[0].is_rate_need()
     p_dir=mk_save_dirs(self.__save_parent_dir,*save_p_dirs)
     
     if not is_need_sort:
          #ソートなし
          f_full_name=p_dir+dir_border_char+file_name_part+".csv"
          with open(f_full_name,mode,encoding="utf_8_sig") as f:
             print(content,file=f)
             header=content.replace("別","名")+","+ResultWriter.decide_item_order(0)
             print(header,file=f)
             for one_item_data in write_data:
               print(one_item_data,file=f)
             
             print("\n\n",file=f)
             f.close()
             
          return
      
     #以下はソートが必要な場合
     #年・月・日を扱う場合は,rate(活動率）については調べる必要ないため、  sort_itemsからrateは除く
     sort_items=("number","size","rate") if is_need_rate else ("number","size")
       
     for item_index,sort_item in enumerate(sort_items):
            f_name=p_dir+dir_border_char+file_name_part+sort_item+".csv"
            with open(f_name,mode,encoding="utf_8_sig") as f:
            
              #decide_item_orderは,csvのheaderの順番を決めるためのもの
              #例えば,ファイルサイズでソートしたときは（sort_itemがsizeの時は),headerを"日付,合計サイズ(KB),写真の合計枚数,活動率,という文字列にしなければならない)
              item_order=ResultWriter.decide_item_order(item_index)
              print(item_order.split(",")[0]+"ソート",file=f)
              print(content,file=f)
              header=content.replace("別","名")+","+item_order
              print(header,file=f)
              sort_result=DataByDate.sort(write_data,sort_item)
              for one_result in sort_result:
                 print(one_result,file=f)
                 
              print("\n\n",file=f)
              f.close()
   
   #年に関係なく月・日のデータに関して,年別の内訳を出す            
   def __fwrite_special(self,write_data:tuple,find_data:tuple,save_p_dirs:tuple,file_name_part:str,mode:str,content:str):
   
      is_need_rate=write_data[0].is_rate_need()
      p_dir=mk_save_dirs(self.__save_parent_dir,*save_p_dirs)
      
      sort_items=("number","size","rate") if is_need_rate else ("number","size")
      for item_index,sort_item in enumerate(sort_items):
         f_name=p_dir+dir_border_char+file_name_part+sort_item+".csv"
         with open(f_name,mode,encoding="utf_8_sig") as f:
           print(ResultWriter.decide_item_order(item_index).split(",")[0]+"ソート",file=f)
           print(content,file=f)
           #まずは,headerとして活動していた年名を出す
           header=content.replace("別","名")+",全ての年の合計"
           for year_name in range(self.__start_date["year"],self.__goal_date["year"]+1):
              header += (","+"%d年"%(year_name))
           print(header,file=f)
           
           sorted_data=DataByDate.sort(write_data,sort_item)
           
           #ここから各月日のみ、月のみデータに対して年ごとの内訳を計算
           
           for one_data in sorted_data:
             #年ありのすべてのデータを、現在の年なしのデータのメソッドの引数として与え、与えた年ありのデータの中から、年なしのデータと月・日が一致するものを絞り込んでリストとして返す
             same_month_date_data=one_data.get_same_month_date_data_regardless_year(find_data)
             month_str="%d月"%(one_data.month) if one_data.month is not None else ""
             date_str="%d日"%(one_data.date) if one_data.date is not None else ""
             
             one_data.set_mode(sort_item)
             one_row=month_str+date_str+","+one_data.get_result_in_str_in_current_mode()
             data_ind=0
             
             #年別のデータを出す
             for year_name in range(self.__start_date["year"],self.__goal_date["year"]+1):
              
                #same_month_date_dataというところに、今扱っている月（日）と同じ月（日）が与えられている年ありデータが入っている
                #これはもう年順にソートされている
                #ここでは、活動していた期間に存在する年を1年ずつ見てゆき、その年のデータが存在したら,その年のデータを引っ張り出す
                
                if data_ind < len(same_month_date_data) and year_name  ==  same_month_date_data[data_ind].year:
                   same_month_date_data[data_ind].set_mode(sort_item)
                   date_str=","+same_month_date_data[data_ind].get_result_in_str_in_current_mode()
                   one_row += date_str
                   data_ind += 1
                   continue
                #もし、その年のデータがなければ,その時のデータは0なので,0を埋める(csvのため埋めなければならない)  
                provisonal_data=DataByDate.get_zero_str_in_current_mode(sort_item)
                one_row += (","+provisonal_data)
             
             print(one_row,file=f)
           
           print("\n\n",file=f)
           f.close()  
                
                 
                
   def __fwrite_no_files_days(self):
     p_dir=mk_save_dirs(self.__save_parent_dir,*("non_year_month","sort"))
     no_files_days_file="photo_analayse_result_non_file_exists_dates_regardless_year.csv"
     
     with open(p_dir+dir_border_char+no_files_days_file,"w",encoding="utf_8_sig") as f:
       print("1枚も写真がなかった日一覧",file=f)
       #1行に5日分ずつ記す
       print("月名,,,,,",file=f)
       for month_name in range(1,12+1):
         #no_files_daysというディクトには現在,{"月名1":["月日名","月日名",・・],"月名2":["月日名","月日名"・・]}という構造にて,写真が1枚もなかった日が格納されている。
         #つまり以下のディクトの無活動日にアクセスするには,"〇（月名の数字)月"という文字列のキーを作らなければならない
         key_str="%d月"%(month_name)
         
         if key_str not in self.__no_files_days.keys():
           print(key_str+",該当日なし,,,,",file=f)
           print(",",file=f)
           continue
           
         one_month_no_files_days=self.__no_files_days[key_str]
         
         #1行に5日分（カンマ5つ分）書きたいが、無活動日が5の倍数であるとは限らない。
         #ゆえに、無活動日の日数から最も近い5の倍数を得る
         
         no_files_days_num=len(one_month_no_files_days)
         comma_num=(int(no_files_days_num/5)+1)*5
         
         #月名
         print(key_str,file=f,end=",")
         
         #1行に5日分ずつ表す。
         for i in range(0,comma_num):
           last_comma="\n," if i % 5 == 4 else ","
           try:
             print(one_month_no_files_days[i]+last_comma,file=f,end="")
           #無活動日の日数目から最も近い5の倍数までは、カンマだけを入れる
           except IndexError:
             print(last_comma,file=f,end="")
         
         print("\n",file=f,end="")
      
       print("\n\n",file=f)
       f.close()   
     
   #曜日と時間帯ごとのファイル数・サイズ・活動率（曜日のみ）のデータを出力（ただし、ソートはしない)
   def f_write_by_weekdays_and_hour(self):
   
      #各曜日のデータ
      #すべて0番目が月曜、1番目が火曜日、・・6番目が日曜日となっている
      #曜日ごとのファイル数
      data_by_weekdays_file_num=self.__f_analyser.days_files
      #曜日ごとのファイルサイズ
      data_by_weekdays_size=self.__f_analyser.days_size
      #曜日ごとの活動率(リストの中に入れ子で,[{"all":期間中の月曜日の数,"file_exists":月曜日の活動数"},{"all":期間中の火曜日の数,"file_exists":火曜日の活動数"},・・]という感じで入っている)
      data_by_weekdays_rate=self.__f_analyser.get_exists_file_weekdays_rate()
      
      p_dir=mk_save_dirs(self.__save_parent_dir,"other")
      
      f_name=p_dir+dir_border_char+"analyse_result_by_weekdays_and_hours.csv"
      with open(f_name,"w",encoding="utf_8_sig") as f:
        print("曜日別データ",file=f)
        print("曜日名,写真の合計枚数,合計サイズ(KB),その曜日の活動率(%),その曜日の活動日数,期間中のその曜日の全日数",file=f)
        for day_ind in range(7):
           day_f_num=data_by_weekdays_file_num[day_ind]
           day_size=data_by_weekdays_size[day_ind]
           day_rate_data=data_by_weekdays_rate[day_ind]
           all_weekday_num=day_rate_data["all"]
           f_exists_weekday_num=day_rate_data["file_exists"]
           d_rate=f_exists_weekday_num/all_weekday_num
           print("%s曜日,%d,%.3f,%.2f%%,%d,%d"%(WEEKDAYS_NAME[day_ind],day_f_num,day_size/(10**3),d_rate,f_exists_weekday_num,all_weekday_num),file=f)
        
        print("\n\n",file=f)
        
        print("時間帯別データ",file=f)
        print("時間帯,写真の合計枚数,合計サイズ(KB)",file=f)
        f_num_by_hours=self.__f_analyser.files_by_hours
        f_size_by_hours=self.__f_analyser.size_by_hours
        for hour in range(24):
           print("%d時台,%d,%.3f"%(hour,f_num_by_hours[hour],f_size_by_hours[hour]),file=f)
        
        print("\n\n",file=f)
        f.close()
       
        
      
   
   #実際にcsvにするとき、ソートした項目を一番前にする 
   #例えば、ソートしてないときや、単純にファイルの数でソートした場合はcsvのheaderは,"日付, 写真の合計枚数, 合計サイズ(KB),活動率(%),活動日数,合計日数"という順番
   #ファイルの大きさでソートしたときのcsvのheaderは,"日付,合計サイズ(KB),写真の合計枚数,活動率(%),活動日数,合計日数"という順番
   #活動率でソートしたときは,"日付,活動率(%),活動日数,合計日数,写真の合計枚数,合計サイズ(KB)"とする
   #item_indexという変数で、今どの項目でソートしているかを表す.(0はファイル数,1はファイルサイズ,2は活動率
   @classmethod 
   def decide_item_order(cls,item_index):
     
     items=["写真の合計枚数","合計サイズ(KB)","活動率(%),活動日数,合計日数"]
    
     item_order=items.pop(item_index)
     for remaining_item in items:
       item_order += (","+remaining_item)
     
     return item_order
        
     