#encoding:utf-8

import math

class MyFraction:

     def __init__(self,one,two=None):
   
       self.numerator=1
       self.denominator=1
       self.fraction_str=""
       if two is None:
       
         if type(one) == str:
           if "/" not in one:
              raise ValueError("the argument is improper. we can only accept an string including "/" or more than one integers")
              
           self.fraction_str=one
           fraction_nums=one.split("/")
           try:
             self.numerator=int(fraction_nums[0])
             self.denominator=int(fraction_nums[1])
           except ValueError:
              raise ValueError("both the numerator and the denominator must be integer")
         
         elif type (one) == int:
            self.numerator=one
       else:
           if type(one) != int or type(two) != int:
              raise ValueError("both the numerator and the denominator must be integer")
           
           self.numerator=one
           self.denominator=two
           
       
       if self.denominator == 0:
           raise ValueError("the denominator must not be zero.")
        
       if self.denominator < 0:
         self.denominator=(-1)*self.denominator
         self.numerator=(-1)*self.numerator
       
           
       self.reduction()
       self.fraction_str="%d/%d"%(self.numerator,self.denominator)
       if self.denominator == 1:
          self.fraction_str="%d"%(self.numerator)
            
         
    
     def reduction(self):
       gcd=MyFraction.getGCD(self.numerator,self.denominator)
       if (gcd !=1 and gcd != -1) or (self.numerator < 0 and self.denominator < 0):
          if gcd < 0:
            gcd=(-1)*(gcd)
            
          self.numerator=int(self.numerator/gcd)
          self.denominator=int(self.denominator/gcd)
    
     def getCommonFraction(self,other):
     
       lcm=(self.denominator*other.denominator)/MyFraction.getGCD(self.denominator,other.denominator)
       new_denominator=int(lcm)
       new_numerator_self=self.numerator*int(new_denominator/self.denominator)
       new_numerator_other=other.numerator*int(new_denominator/other.denominator)
          
       return new_denominator,new_numerator_self,new_numerator_other
          
       
     def __add__(self,other):
     
       if type(other) == int:
          other=MyFraction(other)
          
       if type(other) == float:
           return self.__float__()+other
       
       if type(other) == MyFraction:
          
          new_denominator,new_numerator_self,new_numerator_other=self.getCommonFraction(other)
          
          
          return MyFraction(new_numerator_self+new_numerator_other,new_denominator)
     
     def __radd__(self,other):
        
         return self.__add__(other)
     
     def __sub__(self,other):
    
       if type(other) == int:
          other=MyFraction(other)
          
       if type(other) == float:
           return self.__float__()-other
       
       if type(other) == MyFraction:
       
          new_denominator,new_numerator_self,new_numerator_other=self.getCommonFraction(other)
          
          
          return MyFraction(new_numerator_self-new_numerator_other,new_denominator)
     
     def __rsub__(self,other):
      
      if type(other) == int:
          other=MyFraction(other)
          
      if type(other) == float:
           return other-self.__float__()
       
      if type(other) == MyFraction:
       
          new_denominator,new_numerator_self,new_numerator_other=self.getCommonFraction(other)
          
          return MyFraction(new_numerator_other-new_other_self,new_denominator)
    
     def __mul__(self,other):
    
         if type(other) == int:
           other=MyFraction(other)
           
         if type(other) == float:
           return self.__float__()*other
           
         if type(other) == MyFraction:
            
             return MyFraction(int(self.numerator*other.numerator),int(self.denominator*other.denominator))
      
     def __rmul__(self,other):
     
        return self.__mul__(other) 
     
     def __truediv__(self,other):
          
         if type(other) == int:
           other=MyFraction(other)
         
         if type(other) == float:
           return self.__float__()/other
           
         if type(other) == MyFraction:
            
             return MyFraction(int(self.numerator*other.denominator),int(self.denominator*other.numerator))
     
     def __rtruediv__(self,other):
     
        if type(other) == int:
           other=MyFraction(other)
         
        if type(other) == float:
           return other/self.__float__()
           
        if type(other) == MyFraction:
           return MyFraction(int(other.numerator*self.denominator),int(other.denominator*self.numerator))
     
     def __mod__(self,other):
       
        if type(other) == int:
          other=MyFraction(other)
        
        if type(other) == MyFraction:
            g,m=self.__divmod__(other)
            return m
            
     def __rmod__(self,other):
     
       if type(other) == int:
          other=MyFraction(other)
        
       if type(other) == MyFraction:
            g,m=other.__divmod__(self)
            return m
     
     def __floordiv__(self,other):
     
        if type(other) == int:
           other=MyFraction(other)
        
        if type(other) == float:
           return int(self.__float__()/other)
        
        if type(other) == MyFraction:
            
            q,m=self.__divmod__(other)
            return q
     
     def __rfloordiv__(self,other):
     
       if type(other) == int:
           other=MyFraction(other)
        
       if type(other) == float:
           return int(other/self.__float__())
        
       if type(other) == MyFraction:
            
            q,m=other.__divmod__(self)
            return q
      
     def __divmod__(self,other):
       
       self_value=self.numerator/self.denominator
       other_value=other.numerator/other.denominator
       
       operand_accord_pos_neg=True
       
       tmp_true_div=self.__truediv__(other)
       
       if tmp_true_div.denominator == 1:
           quotient=tmp_true_div.numerator
           
       else:
         
         if self_value < 0:
           self_value=(-1)*(self_value)
           operand_accord_pos_neg=not(operand_accord_pos_neg)
           
         
         if other_value < 0:
            other_value=(-1)*(other_value)
            operand_accord_pos_neg=not(operand_accord_pos_neg)
         
         sum=other_value
         quotient=0
         
         while sum <= self_value:
            quotient += 1
            sum += other_value
         
         
         if not operand_accord_pos_neg:
            quotient=(-1)*(quotient+1)
            
       modulus=self.__sub__(other.__mul__(quotient))
       
       return quotient,modulus
          
     def __pow__(self,other):
     
         if type(other) == int:
           if other > 0:
            return MyFraction(self.numerator**other,self.denominator**other)
           elif other < 0:
            pos_other=-(other)
            return MyFraction(self.denominator**pos_other,self.numerator**pos_other)
           else:
             return MyFraction(1)
         
         if type(other) == float:
           return self.__float__()**other
         
         if type(other) == MyFraction:
            return self.__float__()**other.__float__()
         
         return 1
     
     def __rpow__(self,other):
       
       if type(other) == MyFraction:
         return other.__float__()**self.__float__()
         
       
       return other**self.__float__()
     
     def __invert__(self):
        
          return self.getReciprocal()
     
     def __neg__(self):
          return MyFraction(-self.numerator,self.denominator)
         
     def getReciprocal(self):
          return MyFraction(self.denominator,self.numerator)
     

     def copy(self):
     
         return MyFraction(self.numerator,self.denominator)
    
     def __str__(self):
          return self.fraction_str
     
     def __repr__(self):
        
         return "%s(%d,%d)"%(self.__class__.__name__,self.numerator,self.denominator)
     
     def __eq__(self,other):
        
        if type(other) == MyFraction:
           return self.numerator == other.numerator and self.denominator == other.denominator
        
        self_value=self.__float__()
        
        return self_value==other
     
     def __ne__(self,other):
     
       return not (self.__eq__(other))
       
     def __lt__(self,other):
     
       a,new_numerator_self,new_numerator_other=self.getCommonFraction(other)
       
       return new_numerator_self < new_numerator_other
     
     def __gt__(self,other):
     
       a,new_numerator_self,new_numerator_other=self.getCommonFraction(other)
       
       return new_numerator_self > new_numerator_other
     
     
     def __le__(self,other):
     
       a,new_numerator_self,new_numerator_other=self.getCommonFraction(other)
       
       return new_numerator_self <= new_numerator_other
     
     def __ge__(self,other):
     
       a,new_numerator_self,new_numerator_other=self.getCommonFraction(other)
       
       return new_numerator_self >= new_numerator_other
         
     
     def __float__(self):
        return self.numerator/self.denominator
     
     
     def __int__(self):
        return int(self.__float__())
           
     
     @classmethod
     def getGCD(cls,num1,num2):
        a=max(num1,num2)
        b=min(num1,num2)
        
        while b !=0:
          result=a%b
          a=b
          b=result
        
        return a
       
     
     

def getDigitNum(num):
   return int(math.log10(num))+1


def logCalc(num):
    return math.log(num,10) == math.log10(num)


def beyond(cond1,cond2):
    return (cond1 and not cond2) or (not cond1 and cond2)
    
def eq(cond1,cond2):
    return (cond1 and cond2) or (not cond1 and not cond2)


def condif(cond1,cond2):
    return not cond1 or cond2 