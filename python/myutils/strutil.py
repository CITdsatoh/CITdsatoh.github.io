#encoding:utf-8

from operator import xor
from math import ceil

def int_to_str(num:int,base=10,is_lower=True):
  
  result=""
  digit=1
  
  if base < 2 or 36 < base:
     return None
  
  num_positive=abs(num)
  
  while digit <= num_positive:
    
    dig_num=int(num_positive/digit)%base
    dig_str=num_to_chr(dig_num,is_lower)
    result=dig_str+result
    digit *=base
  
  if num < 0:
     result="-"+result
     
  if len(result) == 0:
     return "0"
     
  return result
 

def num_to_chr(num:int,is_lower):
  if num >= 0  and num < 10:
    return chr(ord("0")+num)
  
  a_ord=ord("a") if is_lower else ord("A")
  
  return chr(a_ord+(num-10))
  

class StrRange:

   def __init__(self,start=0,goal=None,step=None,base=None):
    
    
    if step == 0:
      raise ValueError()
    
    self.is_lower=True
    self.step=1 if step is None else step
    self.base=10 if base is None else base
    self.goal=start if goal is None else goal
    
    
    self.start=0 if goal is None else start
    if type(self.start) != int:
      only_alpha="".join([ch for ch in self.start if ch.isalpha()])
      self.is_lower=not(only_alpha.isupper())
      is_upper=only_alpha.isupper()
      while  self.base < 36:
       try:
        self.start=int(self.start,self.base)
       except ValueError:
        self.base=16 if self.base == 10 else self.base+1 
       else:
        break
    
    if type(self.goal) != int:
      only_alpha="".join([ch for ch in self.goal if ch.isalpha()])
      self.is_lower=not(only_alpha.isupper()) and self.is_lower
      while  self.base < 36:
       try:
        self.goal=int(self.goal,self.base)
       except ValueError:
         self.base=16 if self.base == 10 else  self.base+1
       else:
         break
    
    self.now_num=self.start
    self.is_up=(0 < self.step)
    
    
   def __str__(self):
   
     result=""
     while True:
       try:
         value=self.__next__()
       except StopIteration:
         return "["+result[0:len(result)-1]+"]"
       else:
         result+=(value+",")
   
   def copy(self):
      return eval(self.__repr__())
   
   def __getitem__(self,key):
      if self.__len__() <= key:
         raise IndexError("StrRange object index out of range")
      
      value=int_to_str(self.start+(self.step*key),self.base,self.is_lower)
      
      return value
       
   def __iter__(self):
      return self
   
   def __len__(self):
     
     ret=int(ceil((self.goal-self.start)/self.step))
     
     if ret < 0:
       ret=0
     
     return ret
      
   def __repr__(self):
   
      return "%s(%d,%d,%d,%d)"%(self.__class__.__name__,self.start,self.goal,self.step,self.base)
   
   def __eq__(self,other):
      
      if type(other) != type(self):
          return False
      
      return (self.step == other.step) and (self.start == other.start) and (self.goal == other.goal) and (self.base == other.base)
      
   def __next__(self):
     
      if (self.goal <= self.now_num  and self.is_up) or( not self.is_up and self.now_num <= self.goal ):
        self.now_num=self.start
        raise StopIteration()
      
      value=int_to_str(self.now_num,self.base,self.is_lower)
      
      self.now_num += self.step
      
      return value
    
   
   
    
      
     
