#encoding:utf-8


class DataByDate:
   
    def __init__(self,ymd:tuple,f_num_sum,f_size_sum,rate:tuple=None):
      
       self.__year=ymd[0]
       self.__month=ymd[1]
       self.__date=ymd[2]
       
       self.__f_num_sum=f_num_sum
       self.__f_size_sum=f_size_sum
       
       #rate（0番目：その期間の全日数,1番目:その期間中のファイルが存在した日,2番目、1番目/0番目の値(割合)
       #が引数として与えられなかったとき,その日は活動していたことが自明なので,
       self.__all_days=1
       self.__f_exists_day=1
       self.__rate=1.0
       
       self.__rate_data=rate
       
       if self.__rate_data is not None:
         self.__all_days=rate[0]
         self.__f_exists_day=rate[1]
         self.__rate=rate[2]
          
       self.__mode="number"
    
    def set_mode(self,mode):
       if mode in ("number","size","rate","date"):
          self.__mode=mode
    
    def __lt__(self,other):

       if type(self) == type(other):
         if self.__mode == "number":
            return self.__f_num_sum < other.f_num_sum
         
         if self.__mode == "size":
            return self.__f_size_sum < other.f_size_sum
         
         if self.__mode == "rate":
            return self.__rate < other.rate
         
         #日付順の比較
         if self.__mode == "date":
            #2つのオブジェクトの年が違うなら(2つとも両方ともNoneである場合も除外）
            if self.__year != other.year and (self.__year is not  None or other.year is not None):
            
               #自分か、相手かどちらか一方がNoneであった場合は
               #その時は、Noneの方を早いものとして扱う
               if self.__year is None or other.year is None:
                 return self.__year is None and other.year is not None
                 
               #両方ともNoneでない場合は、どちらも異なった年が入っているので当然早い方がTrue
               return self.__year < other.year
               
            
            #もし、2つの年が同じか,どちらか、あるいはどちらもNone(年が与えられておらず、月日のみを考える場合）なら
            
            #月についても年と同じようにして考える(まず、月が異なるかを見る.両方Noneの場合も違うものとして考える)
            if  self.__month != other.month and (self.__month  is not None or other.month is None):
            
                 if self.__month  is None or other.month is None:
                    return self.__month is None and other.month is not None
                 
                 return self.__month < other.month
            
            #日についても同様
            if self.__date != other.date and (self.__date is not None or other.date is not None):
                 
                 if self.__date is None or other.date is None:
                    return self.__date is None and other.date is not None
                 
                 return self.__date < other.date
            
            #ここまで来るのは,年・月・日がすべて一緒（両方Noneも一緒扱い)、あるいはすべてNoneの時である
            #このメソッドは「より」早い方にTrueを返すが、「等しい」場合は、「より」早いのうちに入らない、よってFalseを返す
            return False
                
               
           
       #「等しい」場合は、「より」早い（小さい）のうちに入らないので、Falseを返す
       return False
    
    def __gt__(self,other):
    
      if type(self) == type(other):
      
         if self.__mode == "number":
           return self.__f_num_sum > other.f_num_sum
           
         if self.__mode == "size":
           return self.__f_size_sum > other.f_size_sum
           
         if self.__mode == "rate":    
           return self.__rate > other.rate
         
        #日付順の比較
         if self.__mode == "date":
            #2つのオブジェクトの年が違うなら(2つとも両方ともNoneである場合も除外）
            if self.__year != other.year and (self.__year is not  None or other.year is not None):
            
               #自分か、相手かどちらか一方がNoneであった場合は
               #その時は、Noneの方を早いものとして扱う(Noneの方をFalseとする)
               if self.__year is None or other.year is None:
                 return self.__year is not  None and other.year is None
                 
               #両方ともNoneでない場合は、どちらも異なった年が入っているので当然早い方がTrue
               return self.__year > other.year
               
            
            #もし、2つの年が同じか,どちらか、あるいはどちらもNone(年が与えられておらず、月日のみを考える場合）なら
            
            #月についても年と同じようにして考える(まず、月が異なるかを見る.両方Noneの場合も違うものとして考える)
            if  self.__month != other.month and (self.__month  is not None or other.month is None):
            
                 if self.__month  is None or other.month is None:
                    return self.__month is not None and other.month is  None
                 
                 return self.__month > other.month
            
            #日についても同様
            if self.__date != other.date and (self.__date is not None or other.date is not None):
                 
                 if self.__date is None or other.date is None:
                    return self.__date is not None and other.date is  None
                 
                 return self.__date > other.date
            
            #ここまで来るのは,年・月・日がすべて一緒（両方Noneも一緒扱い)、あるいはすべてNoneの時である
            #このメソッドは「より遅い」にTrueを返すが、「等しい」場合は、「より遅い」のうちに入らない、よってFalseを返す
            return False
                
       
       
      return False
     
    def __le__(self,other):
       return not self.__gt__(other)
     
    def __ge__(self,other):
       return not self.__lt__(other)
     
    def __eq__(self,other):
       if self is other:
          return True
       
       if type(self) != type(other):
          return False
       
       #以下は同じクラスの別のインスタンスであることを前提に処理を行う.
       if not (self.__year == other.year or (self.__year is None and other.year is None)):
          return False
       if not (self.__month == other.month or (self.__month is None and other.year is None)):
          return False
       if not (self.__date == other.date or (self.__date is None and other.date is None)):
          return False
       
       return True
       
     
    def __ne__(self,oher):
       return not self.__eq__(other)
     
     
    def __str__(self):
        y_str="%d年"%(self.__year) if self.__year is not None else ""
        m_str="%d月"%(self.__month) if self.__month is not None else ""
        d_str="%d日"%(self.__date) if self.__date is not None else ""
        
        y_m_d_str=y_str+m_str+d_str
        
        if self.__rate_data is None:
           #サイズ比較モードになっている場合は,サイズを先頭に持ってきてあげる
           if self.__mode == "size":
             return "%s,%.3f,%d,,,"%(y_m_d_str,self.__f_size_sum/(10**3),self.__f_num_sum)
             
           return "%s,%d,%.3f,,,"%(y_m_d_str,self.__f_num_sum,self.__f_size_sum/(10**3))
        
        #ファイルサイズで並べ替えモードなら,ファイルサイズを先頭にしてあげる
        if self.__mode == "size":
          return "%s,%.3f,%d,%.2f%%,%d,%d"%(y_m_d_str,self.__f_size_sum/(10**3),self.__f_num_sum,self.__rate*100,self.__f_exists_day,self.__all_days)
       
        #活動率で並べ替えモードなら,活動率を先頭にする
        if self.__mode == "rate":
          return "%s,%.2f%%,%d,%d,%d,%.3f"%(y_m_d_str,self.__rate*100,self.__f_exists_day,self.__all_days,self.__f_num_sum,self.__f_size_sum/(10**3))
        
        return "%s,%d,%.3f,%.2f%%,%d,%d"%(y_m_d_str,self.__f_num_sum,self.__f_size_sum/(10**3),self.__rate*100,self.__f_exists_day,self.__all_days)
        
    
    def __repr__(self):
      
       return "mode="+self.__mode+self.__str__()
    
    
    def is_rate_need(self):
      return self.__rate_data is not None
    
    def get_result_in_str_in_current_mode(self):
       if self.__mode == "size":
          return "%.3f"%(self.__f_size_sum/(10**3))
       
       if self.__mode == "rate":
          return "%.2f%%"%(self.__rate*100)
       
       if self.__mode == "date":
          return self.ymd
       
       return "%d"%(self.__f_num_sum)
    
    
    #与えられたタプル(このタプルの中は、すべて当該クラス(DataByDate)と同じでなければならない)の中から、自身と月・日が一致するものを返す。
    
    #例えば、このオブジェクトのyearフィールド（年）が設定されておらず、month(月）のみ、あるいは,month(月)とdate(日)のみ設定されているとする
    #その時、与えられたタプルの各要素の中から,自身と、year（年）の値に関係なく,month(月)・date(日）が一致したオブジェクトを絞り込んで返す。
    #ようは、年に関係なく特定の月、あるいは、特定の月・日の枚数を調べているときに、年別の内訳が欲しくなった時に使う
    
    def get_same_month_date_data_regardless_year(self,date_tuple:tuple):
       same_month_date_list=[]
       for one_date in date_tuple:
          if (self.__year is None or self.__year == one_date.year) and (self.__month == one_date.month) and (self.__date == one_date.date):
            same_month_date_list.append(one_date)
       
       #最後に年の順にソートしておく(昇順)
       same_month_date_list_sorted=DataByDate.sort(tuple(same_month_date_list),"date",True)
       
       return same_month_date_list
       
    
    def __getitem__(self,name):
    
      if name == "number_str":
        return "%d"%(self.__f_num_sum)
      
      if name == "size_str":
        return "%.3f"%(self.__f_size_sum/(10**3))
      
      if name == "rate_str":
        return "%.2f%%"%(self.__rate*100)
      
      if name == "date_str":
        return self.ymd
      
      if name == "number":
         return self.__f_num_sum
      
      if name == "size":
         return self.__f_size_sum
      
      if name == "rate":
         return self.__rate
      
      if name == "date":
         return (self.__year,self.__month,self.__date)
       

        
    @property
    def year(self):
      return self.__year
    
    @property
    def month(self):
      return self.__month
    
    @property
    def date(self):
      return self.__date
      
    @property
    def f_num_sum(self):
      return self.__f_num_sum
    
    @property
    def f_size_sum(self):
      return self.__f_size_sum
    
    @property
    def rate(self):
      return self.__rate
    
    @property
    def ymd(self):
     y_m_d_str=""
     is_str_head=True
       
     if self.__year is not None:
       y__m_d_str="%d"%(self.__year)
       is_str_head=False
       
     for item in (self.__month,self.__date):
       item_str=""
       if item is not None:
         item_str="%d"%(item) if is_str_head else "/%d"%(item)
         is_str_head=False
           
       y_m_d_str += item_str
    
     return y_m_d_str           
    
    @classmethod
    #デフォルトは降順ソート.
    def sort(cls,date_infos_tuple:tuple,mode="number",asc=False):
      for one_info in date_infos_tuple:
         one_info.set_mode(mode)
      
      date_infos=list(date_infos_tuple)
      
      #iは整列済みの最後のインデックス
      for i in range(1,len(date_infos)):
        
        j=i
        #print(mode,"を調べています")
        #print("1個前は",date_infos[j-1][mode])
        #print("1個後は",date_infos[j][mode])
        #min="1個後です" if date_infos[j] < date_infos[j-1] else "1個前です"
        #print("小さい方は",min,"です")
        
        
        while j > 0 and ((date_infos[j-1] < date_infos[j] and not asc) or (date_infos[j-1] > date_infos[j] and asc)):
          date_infos[j-1],date_infos[j]=date_infos[j],date_infos[j-1]
          j -= 1
      
      return date_infos
    
    #年に関係ないとある月・日のデータをとり、その後、年ごとの内訳を出したいとき0の年もある。
    #基本的に0の年は、オブジェクトが作られないため,0の年だとわかったら、代わりに、このメソッドを使って,0の年のデータを表す
    @classmethod
    def get_zero_str_in_current_mode(cls,mode="number"):
      if mode == "size":
         return "%.3f"%(0.0)
      
      if mode == "rate":
         return "%.2f%%"%(0.0)
       
      return "0"     