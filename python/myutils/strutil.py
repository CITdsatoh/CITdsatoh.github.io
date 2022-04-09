#encoding:utf-8


def int_to_str(num:int,base=10):
  
  result=""
  digit=1
  
  if base < 2 or 64 < base:
     return None
  
  num_positive=abs(num)
  
  while digit <= num_positive:
    
    dig_num=int(num_positive/digit)%base
    dig_str=num_to_chr(dig_num)
    result=dig_str+result
    digit *=base
  
  if num < 0:
     result="-"+result
  
  return result
 

def num_to_chr(num:int):
  if num >= 0  and num < 10:
    return chr(ord("0")+num)
  elif num >= 10 and num < 36:
    return chr(ord("A")+(num-10))
  elif num >=36 and num < 62:
    return chr(ord("a")+(num-36))
  elif num == 62:
    return "+"
  elif num == 63:
    return "/"
