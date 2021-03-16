from hitandblow import hit_blow


computer =hit_blow.Computer()

tmp_useranswer = input("各桁の数が相異なるような4桁の数字を入力してください(1234など):")

while not hit_blow.Player.isOk(tmp_useranswer):
   print("数字以外が入力されたか，無効な数字（4桁のうち同じ数字が2つ以上ある）が入力された可能性があります")
   tmp_useranswer = input("再度各桁の数が相異なるような4桁の数字を入力してください(1234など):")

user = hit_blow.User(tmp_useranswer)

print("あなたが入力した数字は",tmp_useranswer,"です")

print("あなたの答えを",tmp_useranswer,"に設定しました")

userhit=0

userblow=0

computerhit=0

computerblow=0

count=1


tmp_userassume=input("次にコンピュータが出したと思う4桁の数字を入力してください:")

while not hit_blow.Player.isOk(tmp_userassume):
   print("数字以外が入力されたか，無効な数字（4桁のうち同じ数字が2つ以上ある）が入力された可能性があります")
   tmp_userassume=input("再度コンピュータが出したと思う4桁の数字を入力してください:")
   
user.setMyAssume(tmp_userassume)

while userhit != 4 and computerhit != 4:
   computerassume=computer.getMyAssume();
   userhit=computer.getHitNum(tmp_userassume);
   userblow=computer.getBlowNum(tmp_userassume);
   
   if userhit == 4 and userblow == 4 :
       print("正解です！私の数字は",computer.myanswer,"です!")
       print("よってあなたの勝ちです")
       print("当てるまで",count,"回かかりましたね")
       break
   else:
       print("あなたが入力した",tmp_userassume,"は",userhit,"ヒット",userblow,"ブローです!")
   
   print("次は私（コンピュータ）の番です")
   print("あなたの数字は",computerassume,"だと思います!")
   computerhit=user.getHitNum(computerassume)
   computerblow=user.getBlowNum(computerassume)
   
   if computerhit == 4 and computerblow == 0 :
       print("ちっ，当てられたか")
       print("そうだよ！！正解は",user.myanswer,"だよっ!!")
       print("ちなみにコンピュータの正解は",computer.myanswer,"だからね!!")
       print("あんたの負けね")
       break
   else:
       print("残念だったね，コンピュータちゃん！！")
       print("ちなみに",computerassume,"は",computerhit,"ヒット",computerblow,"ブローだからね")
       computer.narrowDown(computerhit,computerblow)
   
   count += 1
   tmp_userassume=input("じゃあ,さっきと違うコンピュータが出したと思う4桁の数字を入力してね")
   while not hit_blow.Player.isOk(tmp_userassume):
     print("きちんと数字を入れてね！，あっ，数字でも4桁でなおかつ，同じ数字が2つ以上あるのはだめだからね")
     tmp_userassume=input("再度コンピュータが出したと思う4桁の数字を入力してください:")
   

       
   
   