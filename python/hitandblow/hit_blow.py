import random

class Player:
   
   myanswer="0000"
   myassume="0000"
   
   def __init__(self):
      self.brain=[]
      
      for number in range(123,9876,1):
        str_number=str(number).zfill(4)
        if Player.isOk(str_number):
            self.brain.append(str_number)
      
   def getHitNum(self,opponentnumber):
      hitnum = 0
      for i in range(0,len(opponentnumber)):
        if self.myanswer[i] == opponentnumber[i]:
           hitnum += 1
      return hitnum
   
   def getBlowNum(self,opponentnumber):
      blownum = 0
      for i in range(0,len(self.myanswer)):
         for j in range(0,len(opponentnumber)):
            if i == j :
              continue
            elif self.myanswer[i] == opponentnumber[j]:
              blownum += 1
      
      return blownum
   def setMyAssume(self,num):
      pass
   def setmynumber(self):
       pass
   def getMyAssume(self):
       pass
   def narrowDown(self,myhit,myblow):
       pass
       
   @classmethod
   def isOk(cls,number):
      try:
        tmpint=int(number)
      except ValueError:
        return False
      else:
       if  len(number) != 4:
         return False
       i = 0
       while i < len(number)-1:
         j = i+1
         while j < len(number):
            if i == j :
               continue
            elif number[i] == number[j]:
               return False
            j += 1
            
         i += 1
      return True
      
class User(Player):

   def __init__(self,setnum):
     self.myanswer=setnum
   
   def setMyAssume(self,num):
      self.myassume=num
   
   def getMyAssume(self):
       return self.myassume

class Computer(Player):

   def __init__(self):
     super().__init__()
     self.setmynumber()
   
   def setmynumber(self):
     index=random.randint(0,len(self.brain)-1)
     self.myanswer=self.brain[index]
   
   def getMyAssume(self):
       index = random.randint(0,len(self.brain)-1)
       self.myassume=self.brain[index]
       return self.myassume
   
   def narrowDown(self,myhit,myblow):
       newcandidate=[]
       for candidate in self.brain:
         tmp = User(candidate)
         if (tmp.getHitNum(self.myassume) == myhit) and (tmp.getBlowNum(self.myassume) == myblow):
            newcandidate.append(candidate)
         self.brain=newcandidate
 
         
    