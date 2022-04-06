#encoding:utf-8

class StringBuffer:
  
  def __init__(self,ini_string=""):
    self.str_buffer=ini_string
    self.iter_now_index=0
  
  def append(self,new_str):
   tmp_list=[self.str_buffer,new_str]
   self.str_buffer="".join(tmp_list)
  
  def extend(self,new_buffer):
   if type(new_buffer) != StringBuffer:
     raise ValueError("this buffer can only join the object of \'StringBuffer\'")
   
   self.append(str(new_buffer))
  
  def push(self,new_str):
   tmp_list=[new_str,self.str_buffer]
   self.str_buffer="".join(tmp_list)
  
  def insert(self,index,new_str):
    if index < 0 or index > len(self.str_buffer):
      raise IndexError("string index out of range")
    
    tmp_list=[self.str_buffer[0:index],new_str,self.str_buffer[index:]]
    self.str_buffer="".join(tmp_list)
  
  def set(self,index,new_str):
    if index < 0 or index > len(self.str_buffer):
      raise IndexError("string index out of range")
    
    tmp_list=[]
    if index+len(new_str) < len(self.str_buffer):
      tmp_list=[self.str_buffer[0:index],new_str,self.str_buffer[index+len(new_str):]]
    else:
      tmp_list=[self.str_buffer[0:index],new_str]
    
    self.str_buffer="".join(tmp_list)
    
  def pop(self):
     self.str_buffer=self.str_buffer[0:len(self.str_buffer)-1]
     
  def remove(self,index=None,nums=1):
    if index is None:
       index=len(self.str_buffer)-1
     
    if index < 0 or index+nums-1 > len(self.str_buffer):
      raise IndexError("string index out of range")
    
    if nums < 1:
      raise ValueError("the length of remove string must be more than one")
      
    try:
     tmp_list=[self.str_buffer[0:index],self.str_buffer[index+nums:]]
    except IndexError:
     self.str_buffer=self.str_buffer[0:len(self.str_buffer)-1]
    
    self.str_buffer="".join(tmp_list)
  
  def delete(self,del_str):
    
    try:
      start_index=self.str_buffer.index(del_str)
      fin_index=start_index+len(del_str)
      try:
       tmp_list=[self.str_buffer[0:start_index],self.str_buffer[fin_index:]]
       self.str_buffer="".join(tmp_list)
      except indexError:
       self.str_buffer=self.str_buffer[0:start_index]
    
    except ValueError:
       pass
  
  def deleteAll(self,del_str):
    while del_str in self.str_buffer:
      self.delete(del_str)
  
  
  def rdelete(self,del_str):  
    try:
      start_index=self.str_buffer.rindex(del_str)
      fin_index=start_index+len(del_str)
      try:
       tmp_list=[self.str_buffer[0:start_index],self.str_buffer[fin_index:]]
       self.str_buffer="".join(tmp_list)
      except indexError:
       self.str_buffer=self.str_buffer[0:start_index]
    
    except ValueError:
       pass
          
  def clear(self):
    self.str_buffer=""
    
  def find(self,find_str):
   try:
    index=self.str_buffer.index(find_str)
    return index
   except ValueError:
    return -1
   
  def rfind(self,find_str):
   try:
    index=self.str_buffer.rindex(find_str)
    return index
   except ValueError:
    return -1
  
  def __str__(self): 
     return self.str_buffer
  
  def __len__(self):
      return len(self.str_buffer)
  
  def __repr__(self):
     return "StringBuffer(\""+self.str_buffer+"\")"
  
  def __bool__(self):
     return (self.str_buffer is not None) and (self.str_buffer != "")
     
  
  def __eq__(self,other):
    
    if type(other) == str:
      return other == self.str_buffer
    
    if type(other) != StringBuffer:
      return False
    
    return self.str_buffer == other.str_buffer
  
  def __add__(self,other):
  
    copy_buffer=StringBuffer(self.str_buffer)
    if type(other) == str:
      copy_buffer.append(other)
    elif type(other) == StringBuffer:
      copy_buffer.extend(other)
    else:
      raise TypeError("unsupported operand type(s) for +:\'StringBuffer\' and "+type(other).__name__)
    
    return copy_buffer
  
  def __sub__(self,other):
  
    copy_buffer=StringBuffer(self.str_buffer)
    if type(other) == str:
      copy_buffer.deleteAll(other)
    
    elif type(other) == StringBuffer:
      del_str=str(other)
      copy_buffer.deleteAll(del_str)
    
    else:
     raise TypeError("unsupported operand type(s) for -:\'StringBuffer\' and "+type(other).__name__)
    
    return copy_buffer
  
  def __mul__(self,other):
   
    if type(other) != int :
      raise TypeError("unsupported operand type(s) for *:\'StringBuffer\' and "+type(other).__name__)
    
    new_str=[self.str_buffer for i in  range(other)]
    
    return StringBuffer("".join(new_str))
  
  def __truediv__(self,other):
    
    if type(other) == int:
      ret_buffers=[]
      for i in range(0,len(self.str_buffer),other):
        ret_buffers.append(StringBuffer(self.str_buffer[i:i+other]))
     
      return ret_buffers
     
    if type(other) != str:
       raise TypeError("unsupported operand type(s) for /:\'StringBuffer\' and "+type(other).__name__)
    
    return [StringBuffer(new_str) for new_str in self.str_buffer.split(other)]
  
  def __floordiv__(self,other):
    
    if type(other) == int:
      ret_buffers=[]
      for i in range(0,len(self.str_buffer),other):
        ret_buffers.append(self.str_buffer[i:i+other])
     
      return ret_buffers
     
    if type(other) != str:
       raise TypeError("unsupported operand type(s) for // :\'StringBuffer\' and "+type(other).__name__)
    
    return self.str_buffer.split(other)
  
  def __mod__(self,other):
    if type(other) != str:
       raise TypeError("unsupported operand type(s) for % :\'StringBuffer\' and "+type(other).__name__)
    
    return self.str_buffer.strip(other)
  
  def __pow__(self,other):
    if type(other) != int :
      raise TypeError("unsupported operand type(s) for *:\'StringBuffer\' and "+type(other).__name__)
    
    return[StringBuffer(self.str_buffer) for i in range(other)]
  
  def __iadd__(self,other):
  
    if type(other) == str:
      self.append(other)
    elif type(other) == StringBuffer:
      self.extend(other)
    else:
      raise TypeError("unsupported operand type(s) for +:\'StringBuffer\' and "+type(other).__name__)
    
    return self
  
  def __getitem__(self,key):
  
    if type(key) != int:
       raise TypeError("string indices must be integers")
    
    return self.str_buffer[key]
  
  def __setitem__(self,key,value):
     if type(key) != int:
        raise TypeError("string indices must be integers")
     
     if len(self.str_buffer) <= key:
        raise IndexError("string index out of range")
     
     if len(value) != 1:
        raise ValueError("the length of settable string is only one")
        
     try:
      tmp_list=[self.str_buffer[0:key],value,self.str_buffer[key+1:]]
      self.str_buffer="".join(tmp_list)
     except IndexError:
      tmp_list=[self.str_buffer[0:key],value]
      self.str_buffer="".join(tmp_list)
     
  def __iter__(self):
     return self
  
  def __next__(self):
    
    if len(self.str_buffer) == self.iter_now_index:
       raise  StopIteration()
    
    value=self.str_buffer[self.iter_now_index]
    
    self.iter_now_index += 1
    
    return value
     
     