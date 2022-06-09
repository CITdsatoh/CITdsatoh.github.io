#encoding:utf-8

from operator import xor

def int_to_str(num:int,base=10):
  
  result=""
  digit=1
  
  if base < 2 or 36 < base:
     return None
  
  num_positive=abs(num)
  
  while digit <= num_positive:
    
    dig_num=int(num_positive/digit)%base
    dig_str=num_to_chr(dig_num)
    result=dig_str+result
    digit *=base
  
  if num < 0:
     result="-"+result
     
  if len(result) == 0:
     return "0"
     
  return result
 

def num_to_chr(num:int):
  if num >= 0  and num < 10:
    return chr(ord("0")+num)
  
  return chr(ord("a")+(num-10))
  

class StrRange:

   def __init__(self,start,goal=None,step=None,base=None):
    
    
    if step == 0:
      raise ValueError()
    
    self.step=1 if step is None else step
    self.base=10 if base is None else base
    self.goal=start if goal is None else goal
    
    self.start=0 if goal is None else start
    if type(self.start) != int:
      try:
       self.start=int(self.start,self.base)
      except ValueError:
       self.start=int(self.start,16)
       self.base=16
    
    if type(self.goal) != int:
      try:
       self.goal=int(self.goal,self.base)
      except ValueError:
       self.goal=int(self.goal,16)
       self.base=16
    
    self.now_num=self.start
    self.is_up=(0 < self.step)
    
    if xor(0 < self.step,self.start <= self.goal):
      raise ValueError()
    
   def __str__(self):
   
     result=""
     while True:
       try:
         value=self.__next__()
       except StopIteration:
         return result[0:len(result)-1]
       else:
         result+=(value+",")
       
       
   def __iter__(self):
      return self
   
   def __len__(self):
      return int((self.goal-self.start)/self.step)
      
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
      
      value=int_to_str(self.now_num,self.base)
      
      self.now_num += self.step
      
      return value
    
   
   
    
      
     
