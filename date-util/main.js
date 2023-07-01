const objs={};

let currentOperationObj;


const setData=(()=>{
   objs["date-split-calc"]=new DateSplitCalcCorner("date-split-calc");
   objs["age-n-times-date-calc"]=new AgeNTimesCalcCorner("age-n-times-date-calc");
   currentOperationObj=objs["date-split-calc"];
});

const choiceChange=((event)=>{
   currentOperationObj.setVisible(false);
   objs[event.value].setVisible(true);
   currentOperationObj=objs[event.value];
});

const allInit=(()=>{
   for(let oneCorner of Object.values(objs)){
      oneCorner.resetSettings();
   }
   currentOperationObj.setVisible(false);
   
   const funcRadioButtons=document.querySelectorAll("input[name='func-choice']");
   let iniValue=funcRadioButtons[0].value;
   funcRadioButtons[0].checked=true;
   
   objs[iniValue].setVisible(true);
   currentOperationObj=objs[iniValue];
});
