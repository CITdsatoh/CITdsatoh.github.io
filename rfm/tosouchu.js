function addMoneyrule()
{
    var calc_corner=document.getElementById("money_rules");
    var money_rules=calc_corner.querySelectorAll("p.money_per_second");
    var money_rule_num=money_rules.length;
    
    if(money_rule_num > 3){
         return;
    }
    
    var last=money_rule_num-1;
    var before_money_rule_para=money_rules[last];
    
    var parent_new_money_rule=document.createElement("p");
    parent_new_money_rule.className="money_per_second";
    
   if(money_rule_num == 1){
     parent_new_money_rule.innerHTML='残り時間<input type="text" name="money_rule_change_time1" size="6" maxlength="3">分以降:1秒<input type="text" name="money_per_second_rule1" size="6" maxlength="4">円';
   }
   else if(money_rule_num ==2){
      parent_new_money_rule.innerHTML='残り時間<input type="text" name="money_rule_change_time2" size="6" maxlength="3">分以降:1秒<input type="text" name="money_per_second_rule2" size="6" maxlength="4" >円';
   }
   else if(money_rule_num ==3){
      parent_new_money_rule.innerHTML='残り時間<input type="text" name="money_rule_change_time3" size="6" maxlength="3">分以降:1秒<input type="text" name="money_per_second_rule3" size="6" maxlength="4" >円';
   }
   
   before_money_rule_para.after(parent_new_money_rule);
}


function removeMoneyrule()
{
   var calc_corner=document.getElementById("money_rules");
   var money_rules=calc_corner.querySelectorAll("p.money_per_second");
   var money_rule_num=money_rules.length;
   if (money_rule_num <= 1){
       return;
   }
   var reset_rule=money_rules[money_rule_num-1];
   calc_corner.removeChild(reset_rule);
}

function reset(){
  var input_corner_parent=document.getElementById("calculation");
  var all_inputs=input_corner_parent.querySelectorAll("input");
  for (var one_input of all_inputs){
      one_input.value="";
  }
  var money_rules_parent=document.getElementById("money_rules");
  var money_rules=money_rules_parent.querySelectorAll("p.money_per_second");
  if(money_rules.length > 1){
       for(var i=money_rules.length-1;0<i;i--)
       {
            money_rules_parent.removeChild(money_rules[i]);
        }
  }
  
  var result_message=document.getElementById("result_message")
  result_message.textContent="";
  result_message.style.display="none";
}
  
function dispResult(){
   var result=getResult();
   var result_message_para=document.getElementById("result_message");
   result_message_para.textContent=result;
   result_message_para.style.display="block";
   result_message_para.style.color="black";
   var re=new RegExp("エラー");
   if (re.test(result)){
      result_message_para.style.color="rgb(255, 0, 0)";
   }
}

function dispResultWin(){
  document.querySelector("input[name='remaining_min']").value="0";
  document.querySelector("input[name='remaining_sec']").value="0";
  dispResult();
}


function getResult(){
   var game_time_str=document.querySelector("input[name='game_time']").value;
   var correct_num=new RegExp("^[0-9]{1,4}$")
   
   console.log(game_time_str);
   
   if (isError(game_time_str,correct_num)){
      return "エラー:ゲーム時間の入力が不正です";
    }

   var game_time=parseInt(game_time_str);
   
   var money_rules_change_time=[]
   var money_per_second=[]
   
   var initial_money_rule=document.querySelector("input[name='initial_money_per_second']").value;
   console.log(initial_money_rule)
   
   if(isError(initial_money_rule,correct_num)){
      return "エラー:賞金単価の入力が不正です";
   }
   
   var initial_money_per_second=parseInt(initial_money_rule);
   money_rules_change_time.push(game_time);
   money_per_second.push(initial_money_per_second);
   
   var additional_money_rules_correct_num=new RegExp("^(.{0}|[0-9]{1,4})$");
   var money_rules=document.querySelectorAll("#money_rules p.money_per_second input");
   if(money_rules.length > 1){
      for(var i=1;i<money_rules.length;i+=2){
         new_rule_start_time_str=money_rules[i].value;
         new_money_per_second_str=money_rules[i+1].value;
         if (! (additional_money_rules_correct_num.test(new_rule_start_time_str)&& additional_money_rules_correct_num.test(new_money_per_second_str))){
            return "エラー:賞金単価の変動時間か変動後の金額のどちらかの入力に不正があります。";
          }
         if (!(new_rule_start_time_str.length == 0||new_money_per_second_str.length == 0)){
            new_rule_start_time=parseInt(new_rule_start_time_str);
            new_money_per_second=parseInt(new_money_per_second_str);
            if (game_time < new_rule_start_time){
               return "エラー:賞金単価の変動する時点の残り時間が、ゲームそれ自体の時間を超えています";
            }
            money_rules_change_time.push(new_rule_start_time);
            money_per_second.push(new_money_per_second);
         }
      }
   
   }
   
   var calc_min_str=document.querySelector("input[name='remaining_min']").value;
   var calc_sec_str=document.querySelector("input[name='remaining_sec']").value;
   if(isError(calc_min_str,correct_num) || !(new RegExp("^[0-9]{1,2}$").test(calc_sec_str))){
        return "エラー:計算しようとしている残り時間の入力にエラーがあります";
    }
   
   var calc_min=parseInt(calc_min_str);
   var calc_sec=parseInt(calc_sec_str);
   if(calc_sec_str.length === 0){
      document.querySelector("input[name='remaining_sec']").value="0";
      calc_sec=0;
      calc_sec_str="0";
    }
   
   if( (game_time < calc_min) || (game_time == calc_min && calc_sec > 0))
   {
       return "エラー:計算しようとしている残り時間が、ゲーム全体の時間を超えていますので入力をやり直してください";
   }
   
   if (calc_sec >= 60)
   {
       return "エラー:秒数の指定が不正です";
   }
   
   sort(money_rules_change_time,money_per_second);
   money_rules_change_time.push(0)
   
   console.log(money_rules_change_time)
   
   calc_result_money=CalcMoney(money_rules_change_time,money_per_second,calc_min,calc_sec);
   
   return "残り"+calc_min_str+"分"+calc_sec_str+"秒時点での賞金は"+calc_result_money+"円です";
   

}

function isError(item,correct_num)
{
    return (item.length == 0 || ! (correct_num.test(item)));
}

function CalcMoney(change_time,change_money,calc_min,calc_sec)
{
  calc_time_by_sec=(calc_min*60)+calc_sec;
  search_index=getSearchNum(change_time,calc_min);
  money=0;
  for(var i=0;i<search_index;i++)
  {
      money +=(change_time[i]-change_time[i+1])*60*change_money[i];
   }
   
   money+=((change_time[search_index]*60)-calc_time_by_sec)*change_money[search_index];
   
   return money;
}

function getSearchNum(change_times,calc_min)
{
    for(var i=0;i<change_times.length-1;i++)
    {
        if(calc_min < change_times[i] && calc_min >= change_times[i+1])
        {
            return i;
         }
    }
    
    return 0;
}

function sort(change_time,change_money)
{
   console.log(change_time);
   console.log(change_money);
   
   for(var i=0;i<change_time.length-1;i++)
   {
      max_index=i;
      for (var j=i+1;j<change_time.length;j++){
         if (change_time[max_index]< change_time[j]){
            max_index=j;
          }
       }
       t_temp=change_time[i];
       t_money=change_money[i];
       change_time[i]=change_time[max_index];
       change_money[i]=change_money[max_index];
       change_time[max_index]=t_temp;
       change_money[max_index]=t_money;
   }
   
   console.log(change_time);
   console.log(change_money);
}
 
 