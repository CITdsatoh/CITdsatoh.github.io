//2つの日付計算コーナーのもととなるクラス(抽象クラスかわり)
//ここは両コーナーどちらにもある部品のみを記述し,どちらかにしかないものは各サブクラスで定義
function BaseCalcCorner(cornerName){
    this._cornerName=cornerName;
    
    //この入力コーナーのDOMそのもの
    this._cornerDOM=document.getElementById(`${cornerName}-corner`);
    
    
    //日付入力欄
    this._startYearInput=document.querySelector(`input[name='${cornerName}-start-year'`);
    this._startMonthInput=document.querySelector(`input[name='${cornerName}-start-month']`);
    this._startDayInput=document.querySelector(`input[name='${cornerName}-start-day']`);
    this._endYearInput=document.querySelector(`input[name='${cornerName}-end-year'`);
    this._endMonthInput=document.querySelector(`input[name='${cornerName}-end-month']`);
    this._endDayInput=document.querySelector(`input[name='${cornerName}-end-day']`);
    
    //結果表示欄
    this._resultCorner=document.getElementById(`${cornerName}-result-corner`);
    
    
    
    //開始日の入力取り消しボタン
    this._startCancelButton=document.getElementById(`${cornerName}-start-cancel-button`);
    this._startCancelButton.onclick=(()=>{
        this._startYearInput.value="";
        this._startMonthInput.value="";
        this._startDayInput.value="";
    });
    
    //終了日の入力取り消しボタン
    this._endCancelButton=document.getElementById(`${cornerName}-end-cancel-button`);
    this._endCancelButton.onclick=(()=>{
        this._endYearInput.value="";
        this._endMonthInput.value="";
        this._endDayInput.value="";
    });
    
    //実行ボタン
    this._exeButton=document.getElementById(`${cornerName}-exe-button`);
    this._exeButton.onclick=(()=>{
       this._resultCorner.style.display="none";
       //表示処理自体は異なるが,exeButtonが押されたときに(各サブクラスでオーバーライドした)dispResultを呼ぶということ自体は同じ
       if(this.validate()){
         this.dispResult();
       }
       
    });
    
    //コーナー取り消しボタン
    this._resetButton=document.getElementById(`${cornerName}-reset-button`);
    this._resetButton.onclick=(()=>{
       this.resetSettings();
    });
    
    //入力エラーメッセージ表示欄
    this._errorDispCorner=document.getElementById(`${cornerName}-error-disp-corner`);
    this._errorMessagePara=document.getElementById(`${cornerName}-error-message`);
    
    //日付入力欄が何なのか(=開始日なのか,終了日なのか,計算日なのか)を示すためのもの
    //基本的に,配列として,"start","end",の2文字列あるいは,"target"も入った3文字列で構成される配列要素だが,2つか3つかは計算コーナーによって異なる
    this._inputItems=[];
    //エラーメッセージを表示する際の項目名
    this._inputItemsJapanese=[];
    
    //これ以外は各計算コーナーごとに異なるので,各サブクラスで定義する
    
}

BaseCalcCorner.MonthDays=[0,31,28,31,30,31,30,31,31,30,31,30,31];

BaseCalcCorner.isLeapYear=function(year){
   
   if(year % 400 === 0){
      return true;
   }
   if(year % 100 === 0){
     return false;
   }
   if(year % 4 === 0){
     return true;
   }
   
   return false;
}

BaseCalcCorner.toDateJapaneseStr=function(dateObj){
  let weekDayNum=dateObj.getDay();
  const weekDayJapanese=["日","月","火","水","木","金","土"];
  
  return `${dateObj.getFullYear()}年${dateObj.getMonth()+1}月${dateObj.getDate()}日(${weekDayJapanese[weekDayNum]})`;
}

//エラーチェック処理
//これは各コーナーごとに異なるので,後でオーバーライドする
BaseCalcCorner.prototype.validate=function(){
    return false;
}

//初期化
BaseCalcCorner.prototype.resetSettings=function(){
   this._startYearInput.value="";
   this._startMonthInput.value="";
   this._startDayInput.value="";
   this._endYearInput.value="";
   this._endMonthInput.value="";
   this._endDayInput.value="";
   
   this._errorDispCorner.style.display="none";
   this._errorMessagePara.textContent="";
   
   this._resultCorner.style.display="none";
      
   //それ以外の各クラス独自に存在するDOM部品の初期化はオーバーライド先に記述する
   //なお,オーバーライドする際はこのクラス(継承先から見た場合親クラス)のresetSettingsを必ず呼ぶこと

}



//計算したい内容(コーナー)がラジオボタンで変えられるたびに,コーナーごとの表示非表示を変えるメソッド
//こちらはどちらのコーナーに対しても共通の処理なので,オーバーライドはしない(このまま再利用)
//ただし,ここは表示非表示の制御のみで初期化などは行わない
BaseCalcCorner.prototype.setVisible=function(isVisible){
  let visibility=(isVisible)?"":"none";
  this._cornerDOM.style.display=visibility;
}

//結果の表示
//ここは完全に継承先で処理内容が全く異なるので,ここでは抽象メソッド代わりとして何も実装しない
BaseCalcCorner.prototype.dispResult=function(){
}

//日付が正しいかどうかの判定は全クラス(計算コーナーの種類)共通なのでここで定義し継承先で使いまわす
//日付に問題がなければtrueを問題があるならfalseを返し,日付に関するエラーメッセージの表示もここで行う
//エラーメッセージの表示を呼び出しもとではなく,このメソッドでやるのは,もしそうする場合,いちいち返却値を分けて分岐しなければならなくなるので,記述量が増えてしまうためであるのと,ここでやると,何もしなくてもちょうどエラーメッセージの意味ごとに処理を分岐することができているため
BaseCalcCorner.prototype.isDateValid=function(){

   //年・月・日と対象が変わってもエラーとする基準が同じところ(未入力・余計な文字の入力・小数の入力)は,for文で一気にやる
   const ymdJapanese=["年","月","日"];
   for(let i=0;i<this._inputItems.length;i++){
      let ymdInputs=document.querySelectorAll(`input.${this._cornerName}-${this._inputItems[i]}-date-inputs`);
      for(let j=0;j<ymdInputs.length;j++){
          let inputStr=ymdInputs[j].value.trim();
          if(inputStr.length === 0){
            this._errorDispCorner.style.display="";
            this._errorMessagePara.textContent=`${this._inputItemsJapanese[i]}${ymdJapanese[j]}が入力されていません。${this._inputItemsJapanese[i]}${ymdJapanese[j]}を整数で入力してください`;
            return false;
          }
          if(isNaN(Number(inputStr))){
            this._errorDispCorner.style.display="";
            this._errorMessagePara.textContent=`${this._inputItemsJapanese[i]}${ymdJapanese[j]}に不正な文字列が入力されています。必ず,整数を入力してください`;
            return false;
          }
          if(inputStr.indexOf(".") !== -1){
            this._errorDispCorner.style.display="";
            this._errorMessagePara.textContent=`${this._inputItemsJapanese[i]}${ymdJapanese[j]}に小数を指定することはできません。必ず、整数で入力してください`;
            return false;
          }
      }
   }
   
   //年・月・日ごとにエラーとする基準が異なる箇所は,記述量は増えるが,1つずつ調べる
   //ただし,開始・終了での差はなく,全コーナー共通
   
   let yearsInputs=document.querySelectorAll(`input.${this._cornerName}-year-inputs`);
   let monthsInputs=document.querySelectorAll(`input.${this._cornerName}-month-inputs`);
   let daysInputs=document.querySelectorAll(`input.${this._cornerName}-day-inputs`);
   
   for(let i=0;i<yearsInputs.length;i++){
   
     let inputYear=parseInt(yearsInputs[i].value.trim());
     
     //年は1873年以前は開始でも・終了でもアウト
     if(inputYear < 1873){
        this._errorDispCorner.style.display="";
        this._errorMessagePara.textContent="年として指定できるのは,新暦となった1873年以降のみです。また,西暦は下2桁のみで入力することはできません。その場合は必ず4桁で入力してください";
        return false;
     }
     
     let inputMonth=parseInt(monthsInputs[i].value.trim());
     if(inputMonth < 1 || 12 <inputMonth){
       this._errorDispCorner.style.display="";
       this._errorMessagePara.textContent="1月から12月までの間の月以外の数字が入力されています。月として指定できるのは1から12月までの間のみです";
       return false;
     }
     let inputDay=parseInt(daysInputs[i].value.trim());
     
     //うるう年の2月への対応
     if(BaseCalcCorner.isLeapYear(inputYear) && inputMonth === 2){
        if(inputDay < 1 || 29 < inputDay){
          this._errorDispCorner.style.display="";
          this._errorMessagePara.textContent=`入力された日付が不正です。${inputYear}年${inputMonth}月${inputDay}日という日付は存在しません。有効な日付を入力してください!`;
          return false;
        }
     }
     //閏月以外
     else if(inputDay < 1 || BaseCalcCorner.MonthDays[inputMonth] < inputDay){
        this._errorDispCorner.style.display="";
        this._errorMessagePara.textContent=`入力された日付が不正です。${inputYear}年${inputMonth}月${inputDay}日という日付は存在しません。有効な日付を入力してください!`;
        return false;
     }
   }
   return true;
}




function DateSplitCalcCorner(cornerName){
   BaseCalcCorner.call(this,cornerName);
   
   //何の日付なのかを表す
   this._inputItems=["start","end"];
   this._inputItemsJapanese=["開始","終了"];
   
   //分割数入力
   this._splitNumInput=document.querySelector(`input[name='${cornerName}-num']`);
   //分割数入力取り消しボタン
   this._splitNumResetButton=document.getElementById(`${cornerName}-num-cancel-button`);
   this._splitNumResetButton.onclick=(()=>{
      this._splitNumInput.value="";
   });
   
   //結果表示テーブル
   this._resultDispTable=document.getElementById(`${cornerName}-result-table`);
      
   //開始日表示欄
   this._startDateDispSpan=document.getElementById(`${cornerName}-start-date`);
   //終了日表示欄
   this._endDateDispSpan=document.getElementById(`${cornerName}-end-date`);
   //日数計算結果表示欄
   this._daysBetweenSpan=document.getElementById(`${cornerName}-between`);
}

DateSplitCalcCorner.prototype=Object.create(BaseCalcCorner.prototype,{value:{constructor:DateSplitCalcCorner}});


DateSplitCalcCorner.prototype.validate=function(){
   let splitNumStr=this._splitNumInput.value.trim();
   if(splitNumStr.length === 0){
     this._errorDispCorner.style.display="";
     this._errorMessagePara.textContent="分割数が入力されていません.区間をいくつに分けるのか,2から30までの整数を必ず入力してください!";
     return false;
   }
   //実際に利用するときは整数なので,parseIntで変換するが、ここでは数値に変換できるかどうかを調べる(「あ」とか「a」とか余計な文字列が入っていないかどうかを調べる)のでNumberで変換
   //parseIntだと「a」とかの文字列があった場合,NaNではなく,変換できるところまで変換してしまうため
   if(isNaN(Number(splitNumStr))){
      this._errorDispCorner.style.display="";
      this._errorMessagePara.textContent="分割数に数字以外の文字が入力されています。区間をいくつに分けるのか,2から30までの整数を必ず入力してください!";
      return false;
   }
   //これだと実数(小数点が含まれているときにエラーが出ない(parseIntの時も出ない)ので,別途処理する
   if(splitNumStr.indexOf(".") !== -1){
      this._errorDispCorner.style.display="";
      this._errorMessagePara.textContent="分割数に小数を設定することはできません。区間をいくつに分けるのか,2から30までの整数を必ず入力してください!";
      return false;
   }
   let splitNum=parseInt(splitNumStr);
   if(splitNum < 2 || 30 < splitNum){
      this._errorDispCorner.style.display="";
      this._errorMessagePara.textContent="分割数は必ず2以上30以下の整数に設定してください!";
      return false;
   }
   
   //次に日付のエラー
   //計算対象が変わってもエラーとする基準未入力・余計な文字の入力・小数の入力・おかしな日付(2月30日など))は共通なので,関数で処理
   //なお,エラーメッセージも共通なので,エラーメッセージ表示処理も含んでいる.ゆえに,ここでは,falseを返すのみでよい
   if(!this.isDateValid()){
      return false;
   }
   
   //最後は開始日より終了日のほうが早いかどうか調べ,終了日のほうが早い場合はエラー
   const startDateObj=new Date(parseInt(this._startYearInput.value.trim()),parseInt(this._startMonthInput.value.trim())-1,parseInt(this._startDayInput.value.trim()));
   const endDateObj=new Date(parseInt(this._endYearInput.value.trim()),parseInt(this._endMonthInput.value.trim())-1,parseInt(this._endDayInput.value.trim()));
   
   if(endDateObj.getTime() <= startDateObj.getTime()){
      this._errorDispCorner.style.display="";
      this._errorMessagePara.textContent="入力された終了日が開始日より早い日付になっています。必ず,終了日は開始日より遅い日付にしてください";
      return false;
   }
   
   this._errorDispCorner.style.display="none";
   this._errorMessagePara.textContent="";
   return true;
   
   
}

DateSplitCalcCorner.prototype.resetSettings=function(){

   BaseCalcCorner.prototype.resetSettings.call(this);
   this.clearTable();
   this._splitNumInput.value="";
   this._startDateDispSpan.textContent="";
   this._endDateDispSpan.textContent="";
   this._daysBetweenSpan.textContent="";
}

DateSplitCalcCorner.prototype.clearTable=function(){
   
   const tableBody=this._resultDispTable.querySelector("tbody");
   const tableRows=tableBody.querySelectorAll("tr");
   for(let oneTableRow of tableRows){
       tableBody.removeChild(oneTableRow);
   }

}

//結果表示
//なお,ここではエラーチェック処理(validateメソッド)が呼ばれた後で呼ぶことを前提としているため
//入力は全部正しいものとして行う
DateSplitCalcCorner.prototype.dispResult=function(){
  let startYear=parseInt(this._startYearInput.value.trim());
  let startMonth=parseInt(this._startMonthInput.value.trim());
  let startDay=parseInt(this._startDayInput.value.trim());
  
  let endYear=parseInt(this._endYearInput.value.trim());
  let endMonth=parseInt(this._endMonthInput.value.trim());
  let endDay=parseInt(this._endDayInput.value.trim());
  
  let startDateObj=new Date(startYear,startMonth-1,startDay);
  let endDateObj=new Date(endYear,endMonth-1,endDay);
  
  let splitNum=parseInt(this._splitNumInput.value.trim());
  
  let splitResult=DateSplitCalcCorner.splitPeriodsByN(startDateObj,endDateObj,splitNum);
  
  this._resultCorner.style.display="";
  
  this._startDateDispSpan.textContent=BaseCalcCorner.toDateJapaneseStr(startDateObj);
  this._endDateDispSpan.textContent=BaseCalcCorner.toDateJapaneseStr(endDateObj);
  this._daysBetweenSpan.textContent=`${Math.floor((endDateObj-startDateObj)/86400000)}`;
  
  
  this.clearTable();
  const tbody=this._resultDispTable.querySelector("tbody");
  for(let oneResultForRow of splitResult){
    let oneRow=document.createElement("tr");
    for(let oneCeilResult of oneResultForRow){
      let oneCeil=document.createElement("td");
      oneCeil.textContent=oneCeilResult;
      oneRow.appendChild(oneCeil);
    }
    tbody.appendChild(oneRow);
  }
  
  
}
   
DateSplitCalcCorner.splitPeriodsByN=function(startDate,endDate,splitNum){
  
  let elapsedDays=Math.floor((endDate-startDate)/86400000);
  let splitResult=[];
  let periodLastDates=[];
  
  for(let i=0;i<splitNum;i++){
    let onePeriodStrings=[];
    onePeriodStrings.push(`第${i+1}期`);
    onePeriodStrings.push(`${i+1}/${splitNum}`);
    let periodStartDate;
    if(i === 0){
       periodStartDate=startDate;
    }
    else{
       periodStartDate=new Date(periodLastDates[i-1].getFullYear(),periodLastDates[i-1].getMonth(),periodLastDates[i-1].getDate()+1);
    }
    onePeriodStrings.push(BaseCalcCorner.toDateJapaneseStr(periodStartDate));
    let periodLastDate;
    if(i === splitNum-1){
      periodLastDate=endDate;
    }
    else{
      let passedDays=Math.round((elapsedDays/splitNum)*(i+1));
      periodLastDate=new Date(startDate.getFullYear(),startDate.getMonth(),startDate.getDate()+passedDays);
    }
    periodLastDates.push(periodLastDate);
    onePeriodStrings.push(BaseCalcCorner.toDateJapaneseStr(periodLastDate));
    splitResult.push(onePeriodStrings);
  }
 
  return splitResult;
    

}

function AgeNTimesCalcCorner(cornerName){
   BaseCalcCorner.call(this,cornerName);
   
   this._inputItems=["start","end"];
   this._inputItemsJapanese=["先に生まれた人の生まれた","後に生まれた人の生まれた"];
   
   //何倍かを入力する欄(整数だけでなく小数も受け入れる)
   this._NtimesInput=document.querySelector(`input[name='${cornerName}-times']`);
   
   this._NtimesCancelButton=document.getElementById(`${cornerName}-times-cancel-button`);
   this._NtimesCancelButton.onclick=(()=>{
      this._NtimesInput.value="";
   });
   
   //開始日(早い人の誕生日)の表示欄
   this._olderBirthdaySpan=document.getElementById(`${cornerName}-older-birthday`);
   //終了日(遅い人の誕生日)の表示欄
   this._youngerBirthdaySpan=document.getElementById(`${cornerName}-younger-birthday`);
   
   
   //日数の差表示欄
   this._betweenDaysSpan=document.getElementById(`${cornerName}-between`);
   
   //結果(倍数表示欄)
   this._nTimesDispSpan=document.getElementById(`${cornerName}-n-times`);
   //結果(その倍数になる日付)
   this._resultDate=document.getElementById(`${cornerName}-result-date`);
}

AgeNTimesCalcCorner.prototype=Object.create(BaseCalcCorner.prototype,{value:{constructor:DateSplitCalcCorner}});

AgeNTimesCalcCorner.prototype.validate=function(){

   let nTimesInputStr=this._NtimesInput.value.trim();
   
   if(nTimesInputStr.length === 0){
     this._errorDispCorner.style.display="";
     this._errorMessagePara.textContent="何倍にする日付なのかが入力されていません。必ず1以外の0より大きい数を入力してください。なお,整数でも少数でもどちらでも構いません。";
     return false;
   }
   
   let nTimes=Number(nTimesInputStr);
   
   if(isNaN(nTimes)){
      this._errorDispCorner.style.display="";
      this._errorMessagePara.textContent="倍数に数字以外の文字が入力されています。何倍にするのか,1以外の0より大きい数を必ず入力してください!";
      return false;
   }
   //1の比較は,「1」かもしれないし「1.0」かもしれないのでどちらにも対応できるよう,==で比較
   if(nTimes <= 0.0 || nTimes == 1.0){
      this._errorDispCorner.style.display="";
      this._errorMessagePara.textContent="指定する倍数は必ず1以外の0より大きい数にしてください。1がNGなのは,同じ日付に生まれない限り,同じ年齢になる日は存在しないためです。";
      return false;
   }
   
   //次に日付のエラー
   //年・月・日と対象が変わってもエラーとする基準が同じところ(未入力・余計な文字の入力・小数の入力・変な日付の入力)なので関数で処理
   //エラーメッセージも呼び出し先関数で処理済みなのでここではfalseを返すのみでよい
   if(!this.isDateValid()){
      return false;
   }
   
   
  
   //最後は開始日より終了日のほうが早いかどうか調べ,終了日のほうが早い場合はエラー
   const startDateObj=new Date(parseInt(this._startYearInput.value.trim()),parseInt(this._startMonthInput.value.trim())-1,parseInt(this._startDayInput.value.trim()));
   const endDateObj=new Date(parseInt(this._endYearInput.value.trim()),parseInt(this._endMonthInput.value.trim())-1,parseInt(this._endDayInput.value.trim()));
   
   if(endDateObj.getTime() <= startDateObj.getTime()){
      this._errorDispCorner.style.display="";
      this._errorMessagePara.textContent="後に生まれた人の誕生日が先に生まれた人の誕生日より早い日付になっています。必ず,後に生まれた人の誕生日は先に生まれた人の誕生日より遅い日付にしてください";
      return false;
   }
   
   this._errorDispCorner.style.display="none";
   this._errorMessagePara.textContent="";
   return true;

}
AgeNTimesCalcCorner.prototype.resetSettings=function(){
   BaseCalcCorner.prototype.resetSettings.call(this);
   this._NtimesInput.value="";
   
   //開始日(早い人の誕生日)の表示欄
   this._olderBirthdaySpan.textContent="";
   //終了日(遅い人の誕生日)の表示欄
   this._youngerBirthdaySpan.textContent="";
   //日数の差表示欄
   this._betweenDaysSpan.textContent="";
   
   //結果(倍数表示欄)
   this._nTimesDispSpan.textContent="";
   //結果(その倍数になる日付)
   this._resultDate.textContent="";
}

//結果表示
//なお,ここではエラーチェック処理(validateメソッド)が呼ばれた後で呼ぶことを前提としているため
//入力は全部正しいものとして行う
AgeNTimesCalcCorner.prototype.dispResult=function(){
  let startYear=parseInt(this._startYearInput.value.trim());
  let startMonth=parseInt(this._startMonthInput.value.trim());
  let startDay=parseInt(this._startDayInput.value.trim());
  
  let endYear=parseInt(this._endYearInput.value.trim());
  let endMonth=parseInt(this._endMonthInput.value.trim());
  let endDay=parseInt(this._endDayInput.value.trim());
  
  let startDateObj=new Date(startYear,startMonth-1,startDay);
  let endDateObj=new Date(endYear,endMonth-1,endDay);
  
  let ntimes=Number(this._NtimesInput.value.trim());
  
  let daysElapsed=Math.floor((endDateObj-startDateObj)/86400000);
  let yearsElapsed=endYear-startYear;
  let endYearStartDate=new Date(endYear,startMonth-1,startDay);
  //終了日が,「終了年と同じ年の開始日の同じ月日」より早ければ,丸(終了年-開始年)年経っていないので年数は減算する
  if(endDateObj.getTime() < endYearStartDate.getTime()){
     yearsElapsed--;
     //年以外の日数,つまり,〇年と〇日の〇日の部分を計算するため,年を戻す
     endYearStartDate.setYear(endYear-1);
  }
  //次は日数(年以下の)を計算する
  let daysExceptYear=Math.floor((endDateObj-endYearStartDate)/86400000);
  
  this._resultCorner.style.display="";
  
  this._olderBirthdaySpan.textContent=BaseCalcCorner.toDateJapaneseStr(startDateObj);
  this._youngerBirthdaySpan.textContent=BaseCalcCorner.toDateJapaneseStr(endDateObj);
  
  this._betweenDaysSpan.textContent=`${daysElapsed}日(${yearsElapsed}年と${daysExceptYear}日)`;
  
  let guideFormer="先に生まれた人の年齢";
  let guideLetter="後に生まれた人の年齢";
  
  if(ntimes < 1){
    ntimes=1/ntimes;
    let tmp=guideFormer;
    guideFormer=guideLetter;
    guideLetter=tmp;
  }
  
  //先に生まれた人の年齢が後に生まれた人の年齢のn倍になる日を求めるには,2人の日付の差/(n-1)を後に生まれた人の誕生日に足せばよい
  let addDays=Math.round(daysElapsed/(ntimes-1));
  let resultDateObj=new Date(endYear,endMonth-1,endDay+addDays);
  
  //n倍の部分は,小数の場合,文字列から実数に直した場合,きちんとした数であらわせなくなる恐れがあるので,入力された結果をそのまま用いるものとする
  this._nTimesDispSpan.textContent=`${guideFormer}が${guideLetter}の${this._NtimesInput.value.trim()}倍になる日付は`;
  
  this._resultDate.textContent=BaseCalcCorner.toDateJapaneseStr(resultDateObj);
  
  
}

function DateProgressRateCalcCorner(cornerName){
   BaseCalcCorner.call(this,cornerName);
   
   this._inputItems=["start","end","target"];
   this._inputItemsJapanese=["開始","終了","割合を算出したい日付の"];
   
   //計算日入力
   this._calcTargetYearInput=document.querySelector(`input[name='${cornerName}-target-year']`);
   this._calcTargetMonthInput=document.querySelector(`input[name='${cornerName}-target-month']`);
   this._calcTargetDayInput=document.querySelector(`input[name='${cornerName}-target-day']`);
   
   this._calcTargetDateCancelButton=document.getElementById(`${cornerName}-target-cancel-button`);
   this._calcTargetDateCancelButton.onclick=(()=>{
      this._calcTargetYearInput.value="";
      this._calcTargetMonthInput.value="";
      this._calcTargetDayInput.value="";
   });
   
   //入力された開始日・終了日・計算日の表示欄(他と違ってここでは表示する箇所が複数あるので,idではなくclassで取得)
   this._startDateDispSpans=document.querySelectorAll(`span.${cornerName}-start-date-disps`);
   this._endDateDispSpans=document.querySelectorAll(`span.${cornerName}-end-date-disps`);
   this._calcTargetDateDispSpans=document.querySelectorAll(`span.${cornerName}-target-date-disps`);
   
   //開始日から終了日までの日数表示欄
   this._startEndBetweenDaysSpan=document.getElementById(`${cornerName}-between`);
   
   //開始日から計算日までの日数表示欄
   this._startCalcTargetDayElapsedSpan=document.getElementById(`${cornerName}-elapsed`);
   
   //割合表示欄
   this._rateDispSpan=document.getElementById(`${cornerName}-rate-disp`);

}

DateProgressRateCalcCorner.prototype=Object.create(BaseCalcCorner.prototype,{value:{constructor:DateProgressRateCalcCorner}});

//エラーチェック
DateProgressRateCalcCorner.prototype.validate=function(){
   
   //日付のエラー
   //年・月・日と対象が変わってもエラーとする基準が同じところ(未入力・余計な文字の入力・小数の入力・変な日付の入力)なので関数で処理
   //エラーメッセージも呼び出し先関数で処理済みなのでここではfalseを返すのみでよい
   if(!this.isDateValid()){
      return false;
   }
   
   const startDateObj=new Date(parseInt(this._startYearInput.value.trim()),parseInt(this._startMonthInput.value.trim())-1,parseInt(this._startDayInput.value.trim()));
   const endDateObj=new Date(parseInt(this._endYearInput.value.trim()),parseInt(this._endMonthInput.value.trim())-1,parseInt(this._endDayInput.value.trim()));
   const calcTargetDateObj=new Date(parseInt(this._calcTargetYearInput.value.trim()),parseInt(this._calcTargetMonthInput.value.trim())-1,parseInt(this._calcTargetDayInput.value.trim()));
   
   //必ず,日付の順番は「開始日→計算日→終了日」の順でなければならない
   
   
   //日付が順番通りになるかの確認処理自体は,以下の2つ(「終了日」が「計算日」より早くないか,,「計算日」が「開始日」より遅くないかということを確認)でよいが,
   //「開始日」が「終了日」より早いとき,その旨を出したいので,ここでその処理も加える(↓は消さないこと!)
   if(endDateObj.getTime() <= startDateObj.getTime()){
      this._errorDispCorner.style.display="";
      this._errorMessagePara.textContent="必ず,区間の開始日は区間の終了日より前に設定してください";
      return false;
   }
     
   if(endDateObj.getTime() < calcTargetDateObj.getTime()){
      this._errorDispCorner.style.display="";
      this._errorMessagePara.textContent="計算日(進捗率を計算したい日付)は必ず,区間の終了日の日付より前にしてください";
      return false;
   }
   if(calcTargetDateObj.getTime() < startDateObj.getTime()){
      this._errorDispCorner.style.display="";
      this._errorMessagePara.textContent="計算日(進捗率を計算したい日付)は必ず,区間の開始日の日付より後にしてください";
      return false;
   }
   
   this._errorDispCorner.style.display="none";
   this._errorMessagePara.textContent="";
   return true;
   
}

DateProgressRateCalcCorner.prototype.resetSettings=function(){
   BaseCalcCorner.prototype.resetSettings.call(this);
   
   this._calcTargetYearInput.value="";
   this._calcTargetMonthInput.value="";
   this._calcTargetDayInput.value="";
   
   for(let oneStartDateSpan of this._startDateDispSpans){
      oneStartDateSpan.textContent="";
   }
   
   for(let oneEndDateSpan of this._endDateDispSpans){
      oneEndDateSpan.textContent="";
   }
   
   for(let oneCalcTargetDateSpan of this._calcTargetDateDispSpans){
      oneCalcTargetDateSpan.textContent="";
   }
   
   this._startEndBetweenDaysSpan.textContent="";
   
   //開始日から計算日までの日数表示欄
   this._startCalcTargetDayElapsedSpan.textContent="";
   
   //割合表示欄
   this._rateDispSpan.textContent="";

}

//結果表示
//なお,ここではエラーチェック処理(validateメソッド)が呼ばれた後で呼ぶことを前提としているため
//入力は全部正しいものとして行う
DateProgressRateCalcCorner.prototype.dispResult=function(){
  const startYear=parseInt(this._startYearInput.value.trim());
  const startMonth=parseInt(this._startMonthInput.value.trim())-1;
  const startDay=parseInt(this._startDayInput.value.trim());
  
  const endYear=parseInt(this._endYearInput.value.trim());
  const endMonth=parseInt(this._endMonthInput.value.trim())-1;
  const endDay=parseInt(this._endDayInput.value.trim());
  
  const calcTargetYear=parseInt(this._calcTargetYearInput.value.trim());
  const calcTargetMonth=parseInt(this._calcTargetMonthInput.value.trim())-1;
  const calcTargetDay=parseInt(this._calcTargetDayInput.value.trim());
  
  const startDateObj=new Date(startYear,startMonth,startDay);
  const endDateObj=new Date(endYear,endMonth,endDay);
  const calcTargetDateObj=new Date(calcTargetYear,calcTargetMonth,calcTargetDay);
  
  let startEndBetweenDays=Math.floor((endDateObj-startDateObj)/86400000);
  let startCalcElapsedDays=Math.floor((calcTargetDateObj-startDateObj)/86400000);
  
  let rate=startCalcElapsedDays/startEndBetweenDays;
  let ratePercent=rate*100;
  
  //小数第三位まで表示
  ratePercent=Math.round(ratePercent*1000,1000)/1000;
  
  this._resultCorner.style.display="";
  
  for(let oneStartDateSpan of this._startDateDispSpans){
     oneStartDateSpan.textContent=BaseCalcCorner.toDateJapaneseStr(startDateObj);
  }
   
  for(let oneEndDateSpan of this._endDateDispSpans){
     oneEndDateSpan.textContent=BaseCalcCorner.toDateJapaneseStr(endDateObj);
  }
   
  for(let oneCalcTargetDateSpan of this._calcTargetDateDispSpans){
     oneCalcTargetDateSpan.textContent=BaseCalcCorner.toDateJapaneseStr(calcTargetDateObj);
  }
   
  this._startEndBetweenDaysSpan.textContent=`${startEndBetweenDays}`;
   
  this._startCalcTargetDayElapsedSpan.textContent=`${startCalcElapsedDays}`;
   
  //割合表示欄
  this._rateDispSpan.textContent=`${ratePercent}%`;
  

}

function DateAgeRateCalcCorner(cornerName){
   BaseCalcCorner.call(this,cornerName);
   
   this._inputItems=["start","end","target"];
   
   //日付エラーがあったときの日本語の表示名
   this._inputItemsJapanese=["先に生まれた人の生まれた","後に生まれた人の生まれた","年齢倍率を計算しようとしている日付の"];
   
   this._calcTargetYearInput=document.querySelector(`input[name='${cornerName}-target-year']`);
   this._calcTargetMonthInput=document.querySelector(`input[name='${cornerName}-target-month']`);
   this._calcTargetDayInput=document.querySelector(`input[name='${cornerName}-target-day']`);
   
   this._calcTargetDateCancelButton=document.getElementById(`${cornerName}-target-cancel-button`);
   this._calcTargetDateCancelButton.onclick=(()=>{
      this._calcTargetYearInput.value="";
      this._calcTargetMonthInput.value="";
      this._calcTargetDayInput.value="";
      
   });
   
   this._calcTargetTodayPaddingButton=document.getElementById(`${cornerName}-target-today-padding-button`);
   this._calcTargetTodayPaddingButton.onclick=(()=>{
      const todayObj=new Date();
      this._calcTargetYearInput.value=`${todayObj.getFullYear()}`;
      this._calcTargetMonthInput.value=`${todayObj.getMonth()+1}`;
      this._calcTargetDayInput.value=`${todayObj.getDate()}`;
   });
   
   //入力された誕生日の表示欄
   this._olderBirthdaySpan=document.getElementById(`${cornerName}-older-birthday`);
   this._youngerBirthdaySpan=document.getElementById(`${cornerName}-younger-birthday`);
   //2人の年齢差(日単位で)の表示欄
   this._daysBetweenSpan=document.getElementById(`${cornerName}-between`);
   
   //入力された計算日(倍率を求める基準日)の表示欄(複数個所あるのでquerySelectorAllのclassで取得する)
   this._calcTargetDayDispSpans=document.querySelectorAll(`span.${cornerName}-target-date-disps`);
   
   //割合表示欄(上は「先に生まれた人の年齢に対する後に生まれた人の年齢の倍率(=1より大きい),下は「後に生まれた人の年齢に対する先に生まれた人の年齢の倍率(=1未満))
   this._rateDispOldBaseSpan=document.getElementById(`${cornerName}-result-old-base`);
   this._rateDispYoungBaseSpan=document.getElementById(`${cornerName}-result-young-base`);
   
   
}

DateAgeRateCalcCorner.prototype=Object.create(BaseCalcCorner.prototype,{value:{constructor:DateAgeRateCalcCorner}});

//エラーチェック
DateAgeRateCalcCorner.prototype.validate=function(){

   //日付のエラー
   //年・月・日と対象が変わってもエラーとする基準が同じところ(未入力・余計な文字の入力・小数の入力・変な日付の入力)なので関数で処理
   //エラーメッセージも呼び出し先関数で処理済みなのでここではfalseを返すのみでよい
   if(!this.isDateValid()){
      return false;
   }
   
   //入力された日付の順番は「先に生まれた人の誕生日(開始日)→後に生まれた人の誕生日(終了日)→倍率を計算したい日付」の順序でなければならないのでそれを指摘
   const olderBirthdayObj=new Date(parseInt(this._startYearInput.value.trim()),parseInt(this._startMonthInput.value.trim())-1,parseInt(this._startDayInput.value.trim()));
   const youngerBirthdayObj=new Date(parseInt(this._endYearInput.value.trim()),parseInt(this._endMonthInput.value.trim())-1,parseInt(this._endDayInput.value.trim()));
   const calcTargetDayObj=new Date(parseInt(this._calcTargetYearInput.value.trim()),parseInt(this._calcTargetMonthInput.value.trim())-1,parseInt(this._calcTargetDayInput.value.trim()));
   
   if(youngerBirthdayObj.getTime() <= olderBirthdayObj.getTime()){
      this._errorDispCorner.style.display="";
      this._errorMessagePara.textContent="後に生まれた人の誕生日が先に生まれた人の誕生日より早い日付になっています。必ず,後に生まれた人の誕生日は先に生まれた人の誕生日より遅い日付にしてください";
      return false;
   }
   if(calcTargetDayObj.getTime() <= youngerBirthdayObj.getTime()){
      this._errorDispCorner.style.display="";
      this._errorMessagePara.textContent="計算日(倍率を計算した日付)は必ず後に生まれた人の誕生日より後の日付を設定してください";
      return false;
   }
   
   this._errorDispCorner.style.display="none";
   this._errorMessagePara.textContent="";
   return true;
}

DateAgeRateCalcCorner.prototype.resetSettings=function(){
   BaseCalcCorner.prototype.resetSettings.call(this);
   this._calcTargetYearInput.value="";
   this._calcTargetMonthInput.value="";
   this._calcTargetDayInput.value="";
   this._olderBirthdaySpan.textContent="";
   this._youngerBirthdaySpan.textContent="";
   this._daysBetweenSpan.textContent="";
   
   for(let oneCalcTargetDayDispSpan of this._calcTargetDayDispSpans){
      oneCalcTargetDayDispSpan.textContent="";
   }
   
   this._rateDispOldBaseSpan.textContent="";
   this._rateDispYoungBaseSpan.textContent="";
   
   
}

//計算結果の表示
//エラーチェックメソッドvalidateを呼んだ後で呼び出すので,ここではエラーはない前提で処理を進める
DateAgeRateCalcCorner.prototype.dispResult=function(){
    const olderBirthYear=parseInt(this._startYearInput.value.trim());
    const olderBirthMonth=parseInt(this._startMonthInput.value.trim());
    const olderBirthDay=parseInt(this._startDayInput.value.trim());
    
    const youngerBirthYear=parseInt(this._endYearInput.value.trim());
    const youngerBirthMonth=parseInt(this._endMonthInput.value.trim());
    const youngerBirthDay=parseInt(this._endDayInput.value.trim());
    
    const calcTargetYear=parseInt(this._calcTargetYearInput.value.trim());
    const calcTargetMonth=parseInt(this._calcTargetMonthInput.value.trim());
    const calcTargetDay=parseInt(this._calcTargetDayInput.value.trim());
    
    const olderBirthdateObj=new Date(olderBirthYear,olderBirthMonth-1,olderBirthDay);
    const youngerBirthdateObj=new Date(youngerBirthYear,youngerBirthMonth-1,youngerBirthDay);
    const calcTargetDateObj=new Date(calcTargetYear,calcTargetMonth-1,calcTargetDay);
    
    let elapsedDaysBetweenTwoBirthday=Math.floor((youngerBirthdateObj-olderBirthdateObj)/86400000);
    
    let olderPeopleLivingDaysUntilTarget=Math.floor((calcTargetDateObj-olderBirthdateObj)/86400000);
    let youngerPeopleLivingDaysUntilTarget=Math.floor((calcTargetDateObj-youngerBirthdateObj)/86400000);
    
    let ageRateOldBase=olderPeopleLivingDaysUntilTarget/youngerPeopleLivingDaysUntilTarget;
    //小数第三位まで四捨五入
    ageRateOldBase=Math.round(ageRateOldBase*1000,1000)/1000;
    
    let ageRateYoungBase=youngerPeopleLivingDaysUntilTarget/olderPeopleLivingDaysUntilTarget;
    //小数第二位まで四捨五入
    ageRateYoungBase=Math.round(ageRateYoungBase*1000,1000)/1000;
    
    this._resultCorner.style.display="";
    
    this._olderBirthdaySpan.textContent=BaseCalcCorner.toDateJapaneseStr(olderBirthdateObj);
    this._youngerBirthdaySpan.textContent=BaseCalcCorner.toDateJapaneseStr(youngerBirthdateObj);
    this._daysBetweenSpan.textContent=`${elapsedDaysBetweenTwoBirthday}`;
   
    for(let oneCalcTargetDayDispSpan of this._calcTargetDayDispSpans){
      oneCalcTargetDayDispSpan.textContent=BaseCalcCorner.toDateJapaneseStr(calcTargetDateObj);
    }
   
    this._rateDispOldBaseSpan.textContent=`${ageRateOldBase}`;
    this._rateDispYoungBaseSpan.textContent=`${ageRateYoungBase}`;
}






