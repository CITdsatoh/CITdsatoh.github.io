#encoding:utf-8

from operator import xor
from strutil import int_to_str
import random

class AlphabetArray:
 
     def __init__(self,start="A",goal="z",step=1):
      
      if not (AlphabetArray.isUpper(start) or AlphabetArray.isLower(start)):
         raise ValueError()
      
      if not (AlphabetArray.isUpper(goal) or AlphabetArray.isLower(goal)):
         raise ValueError()
      
      if type(step) != int or step == 0:
         raise ValueError()
      
      
      self.start=start
      self.goal=goal
      self.step=step
      
      self.current_value=""
      self.has_recurred=False
      
      self.is_upper_head=True
      self.is_lower_head=True
      
      if AlphabetArray.isUpper(start):
        self.is_lower_head=False  if AlphabetArray.isLower(goal) else None
      
      if AlphabetArray.isLower(start) :
        self.is_upper_head=False if AlphabetArray.isUpper(goal) else None
      
      self.same_char=self.isSameKindOfChar()
     
     def __len__(self):
     
       if self.same_char and self.isVectorAccord():
           return int(ord(self.goal)-ord(self.start) / self.step)+1
           
       a_ord_num,z_ord_num=self.getStartEndChar()
         
       if 0 < self.step:
         return int(((ord(self.goal)-a_ord_num+1)+(z_ord_num-ord(self.start))+1)/self.step)
         
       return int(((z_ord_num-ord(self.goal)+1)+(ord(self.start)-a_ord_num+1))/-self.step)
         
     
     
     def __iter__(self):
       
         return self
     
     def __next__(self):
        
         
         if self.current_value == self.goal:
           self.has_recurred=False
           self.current_value=""
           raise StopIteration()
          
         
         next_value=self.getNextValue(self.current_value)
         
         if next_value is None:
           self.has_recurred=False
           self.current_value=""
           raise StopIteration()
         
         self.current_value=next_value
         
         return next_value
     
     
     
     def __str__(self):
     
       ret=""
       while True:
         try:
           ret+=self.__next__()
         except StopIteration:
            return ret
       
       return ret
     
     
     def reverse(self):
        tmp=self.start
        self.start=self.goal
        self.goal=tmp
        self.has_recurred=False
        self.current_value=""
        self.step=(-1)*self.step
        if self.isSameKindOfChar():
          self.is_upper_head=None if self.is_upper_head else True
          self.is_lower_head=None if self.is_lower_head else True
        else:
          self.is_upper_head=not(self.is_upper_head)
          self.is_lower_head=not(self.is_lower_head)
      
     def __repr__(self):
        return "AlphabetArray(\""+self.start+"\",\""+self.goal+"\","+int_to_str(self.step)+")"
     
     def getNextValue(self,now_value):
       if now_value == "":
          return self.start
       
       
       new_value_ord=ord(now_value)+self.step
       if self.isSameKindOfChar() and self.isVectorAccord():
          if (0 < self.step and  ord(self.goal) < new_value_ord) or (self.step < 0 and new_value_ord < ord(self.goal)):
              return None
              
          return chr(new_value_ord)
       
       a_lim,z_lim=self.getStartEndChar()  
         
       if 0 < self.step:
         if z_lim < new_value_ord and not self.has_recurred:
           new_value_ord=a_lim+(new_value_ord-z_lim-1)
           self.has_recurred=True
            
         if ord(self.goal) < new_value_ord and self.has_recurred:
           return None
            
         return chr(new_value_ord)
         
       if new_value_ord < a_lim and not self.has_recurred:
            new_value_ord=z_lim-(a_lim-new_value_ord-1)
            self.has_recurred=True
         
       if new_value_ord < ord(self.goal) and self.has_recurred:
           return None
         
       return chr(new_value_ord)
      
        
     
     def getStartEndChar(self):
        if self.isSameUpper():
          return ord("A"),ord("Z")
        
        if self.isSameLower():
          return ord("a"),ord("z")
        
        if xor(self.is_upper_head,0 < self.step):
           return ord("A"),ord("z")
           
        return ord("a"),ord("Z")

      
     def isVectorAccord(self):
       if AlphabetArray.CompareIgnoreCase(self.start,self.goal):
          return 0 < self.step
           
       return self.step < 0
     
     def isSameKindOfChar(self):
       
        return self.isSameUpper() or self.isSameLower()
        
     def __eq__(self,other):
       
        return type(self) == type(other) and self.__str__() == other.__str__()
                
     def random(self):
       copy=AlphabetArray(self.start,self.goal,self.step)
       num=random.randint(0,copy.__len__())
       for i,result in enumerate(copy):
         if i == num:
            return result
         
          
       
     def isSameUpper(self):
         return (self.is_upper_head and self.is_lower_head is None)
     
     def isSameLower(self):
         return (self.is_lower_head and self.is_upper_head is None)
     
     def copy(self):
        
        return eval(self.__repr__())
     
     @classmethod
     def isUpper(cls,char):
       return (ord("A") <= ord(char)) and (ord(char) <= ord("Z"))
     
     @classmethod
     def isLower(cls,char):
       return (ord("a") <= ord(char)) and (ord(char) <= ord("z"))
    
     @classmethod
     def CompareIgnoreCase(cls,chr1,chr2):
        if cls.isUpper(chr1) and cls.isLower(chr2):
           return ord(chr1) < ord(chr2)-32
       
        if cls.isLower(chr1) and cls.isUpper(chr2):
           return ord(chr1)-32 < ord(chr2)
        
        return ord(chr1) < ord(chr2)
    


def int_to_alpha_upper(number,start=0):
   if  number < start or number >= start+26:
      raise ValueError()
   
   return chr(ord("A")+(number-start))


def int_to_alpha_lower(number,start=0):

   if number < start or number >= start+26:
     raise ValueError()
   
   return chr(ord("a")+(number-start))

def int_to_alpha(number,start=0,is_upper_head=True):
    if  number < start or number >= start+52:
       raise ValueError()
    
    
    if not xor(is_upper_head,number < start+26):
       return chr(ord("A")+((number-start)%26))
    
    return chr(ord("a")+((number-start)%26))


def alpha_upper_to_int(alpha,start=0):
    if not AlphabetArray.isUpper(alpha):
        raise ValueError()
    
    return (ord(alpha)-ord("A"))+start

def alpha_lower_to_int(alpha,start=0):
    if not AlphabetArray.isLower(alpha):
        raise ValueError()
    
    return (ord(alpha)-ord("a"))+start



def alpha_to_int(alpha,start=0,is_upper_head=True):
    if not (AlphabetArray.isLower(alpha) or AlphabetArray.isUpper(alpha)):
        raise ValueError()
    
    chr_a="A" if AlphabetArray.isUpper(alpha)else "a"
    
    
    if xor(is_upper_head,AlphabetArray.isLower(alpha)):
       return ord(alpha)-ord(chr_a)+start
       
    return ord(alpha)-ord(chr_a)+start+26    
    
