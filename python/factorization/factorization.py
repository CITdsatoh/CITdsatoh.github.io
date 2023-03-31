#encoding:utf-8;

import pathlib

class MyInteger:

  def __init__(self,num:int):
  
    self.__num=num
    #この数の平方根までの素数リスト
    self.__primes_to_num=MyInteger.get_primes_list_to_sqrt_n(int(self.__num**0.5)+1)
  
  
  def factorize(self):
    i=0
    factors=[]
    num=self.__num
    last=int(self.__num**0.5)+1
    while i < len(self.__primes_to_num):
      if num % self.__primes_to_num[i] == 0:
         factors.append(self.__primes_to_num[i])
         num=int(num/self.__primes_to_num[i])
         continue
      i += 1
    if num != 1:
      factors.append(num)
    
    
    return factors
  
  
  def get_all_divisors(self):
    divisors=[]
    for num in range(1,int(self.__num**0.5)+1):
      if self.__num % num == 0:
         divisors.append(num)
    
    divisors_less_sqrt_n=divisors[::]
    
    for num in reversed(divisors_less_sqrt_n):
      new_num=int(self.__num/num)
      #平方数の場合同じ数が2つ入るので除く
      if new_num != num:
         divisors.append(new_num)
    
    return divisors
  
  def __str__(self):
   factors=self.factorize()
   factor_pow={}
   #素因数分解結果は必ず小さい素数の順に並んでいるので、一つ一つ見て行って前の数字と同じかどうかを見る
   #前と違う数字ならpow(乗数）を1にし、前と同じ数字なら乗数を加算する
   #最初の時はどんな数であっても1乗にならないといけないので,絶対にありえない1を入れておく
   current_num=1
   
   for num in factors:
     if current_num != num:
        factor_pow[num]=1
        current_num=num
     else:
        factor_pow[num]=factor_pow[num]+1
   
   #繰り返しの際の*(掛け算）記号がつかないように最初の1回だけは別にやっておく
   first_factor=factors[0]
   first_pow=factor_pow[first_factor]
   factors_str="%d="%(self.__num)
   if first_pow == 1:
     num_str="%d"%(first_factor)
     factors_str += num_str
   else:
     num_str="%d^%d"%(first_factor,first_pow)
     factors_str += num_str
       
   #辞書は順番を保証しないのでfactorsを1つずつたどっていく
   i=0+first_pow
   while i < len(factors):
     factor=factors[i]
     pow=factor_pow[factor]
     if pow == 1:
       factors_str += "*%d"%(factor)
     else:
       factors_str += "*%d^%d"%(factor,pow)
     
     #powの数だけ同じ数字が続くので次のインデックスはpowつ分進める
     i += pow
    
   return factors_str
        
  def csv_str(self):
    divisors=self.get_all_divisors()
    divisors_str="%d"%(divisors[0])
    for i in range(1,len(divisors)):
      divisors_str += ",%d"%(divisors[i])
    
    divisors_str="\""+divisors_str+"\""
    
    note=""
    if len(divisors) == 2:
       note="素数"
    
    return "%d,%s,%s,%d,%d,%s"%(self.__num,self,divisors_str,len(divisors),sum(divisors),note)
  
  @classmethod
  def csv_str_header(cls):
    return "数,素因数分解結果,約数一覧(1含む),約数の個数(1含む),約数の和(1含む),素数かどうか"
  
  
  @classmethod 
  def get_primes_list_to_sqrt_n(cls,num):
    numbers_to_n=[i for i in range(2,num+1)]
    i=0
    last=int(num**0.5)+1
    while  numbers_to_n[i] < last  and  i < len(numbers_to_n):
      prime=numbers_to_n[i]
      j=i+1
      while j < len(numbers_to_n):
        if numbers_to_n[j] % prime == 0 :
          numbers_to_n.pop(j)
          continue
        j += 1
      i += 1
    
    return numbers_to_n
    
     

if __name__ == "__main__":
   
   
   parent=pathlib.Path("number_prime")
   if not parent.exists():
     parent.mkdir()
   
   main_dir_name="number_prime\\2-9999"
   
   main=pathlib.Path(main_dir_name)
   if not main.exists():
      main.mkdir()
      
   
   file_base_name=main_dir_name+"\\素因数リスト"
   file_tail_name="(2から999まで).csv"
   file_name=file_base_name+file_tail_name
   with open(file_name,"a",encoding="utf_8_sig") as f:
      print(MyInteger.csv_str_header(),file=f)
      f.close()
   
   
   for i in range(2,100000):
     if i % 10000 == 0:
       main_dir_name="number_prime\\%d-%d"%(i,i+9999)
       main=pathlib.Path(main_dir_name)
       if not main.exists():
         main.mkdir()
       file_base_name=main_dir_name+"\\素因数リスト"
     if i % 1000 == 0:
       file_tail_name="(%dから%dまで).csv"%(i,i+999)
       file_name=file_base_name+file_tail_name
       with open(file_name,"a",encoding="utf_8_sig") as f:
          print(MyInteger.csv_str_header(),file=f)
          f.close()
     
     number=MyInteger(i)
     with open(file_name,"a",encoding="utf_8_sig") as f:
      print(number.csv_str_header(),file=f)
      f.close()
     
        

  
  