
function sanitizing(obje){
      let str_obj=""+obje
      return str_obj.replace(/&/g,"&amp;").replace(/"/g,"&quot;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
}


class Nuts{
  
  constructor(no,name,tastes,smooth)
  {
     this.no=no;
     this.name=name;
     this.tastes=[];
     this.taste_num=0;
     for(let one_taste of tastes){
       var value=0;
       if(one_taste > 0){
         value=(one_taste+1)*5;
         this.taste_num++;
       }
       this.tastes.push(value);
     }
     this.smooth=smooth;
  }
  
  getRealTaste(){
    let real_taste=[];
    for(let i=0;i<this.tastes.length;i++){
      real_taste.push(this.tastes[i]-this.tastes[(i+1)%this.tastes.length]);
    }
    return real_taste;
  }
  
  toString(){
    return "No."+thisno+":"+this.name;
 }

}

class Pofin{

 constructor(tastes,smooth){
    this.tastes=tastes;
    this.smooth=smooth;
  }
  
  getLevel(){
    let max_level=0;
    for(let taste_level of this.tastes){
      if(max_level < taste_level){
         max_level=taste_level;
      }
    }
    
    
    return max_level;
    
  }
  getPofinName(){
    
    let tastes_num=0;
    let tastes_level_order=[];
    let max_taste=0;
    const taste_name=["から","しぶ","あま","にが","すっぱ"];
    
    
    for(var i=0;i<this.tastes.length;i++){
       if(this.tastes[i] !== 0){
          tastes_num++
          if(max_taste < this.tastes[i]){
             max_taste=this.tastes[i];
             tastes_level_order.unshift(taste_name[i]);
             continue;
          }
          tastes_level_order.push(taste_name[i]);
       }
   }
   
   if(max_taste >= 50){
      return "まろやか";
   }
   if(max_taste <= 5){
     return "まずい";
   }
   
   switch(tastes_num){
     case 4:
       return "くどい";
       break;
     case 3:
       return "こってり";
       break;
     case 2:
      return tastes_level_order[0]+tastes_level_order[1];
      break;
     case 1:
      return tastes_level_order[0]+"い";
      break;
   }
   
  }
  getRate(){
     var sum=0;
     
     for(var one_taste of this.tastes){
        sum+=one_taste;
     }
     
     var rate=sum/this.smooth;
     
     return Math.round(rate*100)/100;
  }
  
  toString(){
  
    
    let pofin_name=this.getPofinName()+"ポフィン: level:"+this.getLevel()+" ";
    const taste_name=["辛","渋","甘","苦","酸"];
    for(var i=0;i<this.tastes.length;i++){
       pofin_name+=taste_name[i]+":"+this.tastes[i]+" ";
    }
    pofin_name+="滑:"+this.smooth;
    pofin_name+=" 効率:"+this.getRate();
    return pofin_name;
  }
  
}

class PofinMaker{
  
  constructor(){
    this.used_nuts_name=[];
    this.tastes_sum=[0,0,0,0,0];
    this.smooth_sum=0;
    this.originally_pofin_taste_num=0;
  }
  
  addNuts(nuts){
    this.used_nuts_name.push(nuts.name);
    this.smooth_sum +=nuts.smooth;
    if(this.originally_pofin_taste_num < nuts.taste_num){
       this.originally_pofin_taste_num=nuts.taste_num;
    }
    
    let one_nuts_tastes=nuts.getRealTaste();
    for(var i=0;i<this.tastes_sum.length;i++){
      this.tastes_sum[i] += one_nuts_tastes[i];
    }
  }
  
  getPofin(){
    let spilt_time_corner=document.querySelector("input[name='spilt']");
    let spilt_time=parseInt(sanitizing(spilt_time_corner.value));
    if(isNaN(spilt_time)||spilt_time_corner.value.length===0||spilt_time < 0){
      spilt_time=0;
      spilt_time_corner.value="0";
    }
    
    let burnt_time_corner=document.querySelector("input[name='burnt']");
    let burnt_time=parseInt(sanitizing(burnt_time_corner.value));
    if(isNaN(burnt_time)||burnt_time_corner.value.length===0||burnt_time < 0){
      burnt_time=0;
      burnt_time_corner.value="0";
    }
    
    let cooking_time_corner=document.querySelector("input[name='time']");
    let cooking_time=Number(sanitizing(cooking_time_corner.value));
    if(isNaN(cooking_time)||cooking_time_corner.value.length===0||cooking_time > 60){
      cooking_time=60.00;
      cooking_time_corner.value="60.00";
    }
    
    if(cooking_time < 30){
       cooking_time=30.00;
      cooking_time_corner.value="30.00";
    }
    
    let penalty=burnt_time+spilt_time;
    let taste_num_minus=parseInt(Math.floor(this.originally_pofin_taste_num/2))+1;
    let time_bounus=(60.00/cooking_time);
    let real_tastes=[];
    let all_less_five=true;
    
    for(var i=0;i<this.tastes_sum.length;i++){
       var practically_taste_value=parseInt((this.tastes_sum[i]-penalty-taste_num_minus)*time_bounus);
       if(practically_taste_value <= 0){
         real_tastes.push(0);
         continue;
       }
       
       
       if(practically_taste_value > 5){
          all_less_five=false;
       }
       
       if(practically_taste_value > 99){
         real_tastes.push(99);
         continue;
       }
       real_tastes.push(practically_taste_value);
    }
    
    if(all_less_five||PofinMaker.isOverlapNuts(this.used_nuts_name)){
      for(var i=0;i<real_tastes.length;i++){
        real_tastes[i]=parseInt(Math.floor(Math.random()*5));
      }
      
      return new Pofin(real_tastes,this.getSmooth());
    }
    
    
    console.log(this.used_nuts_name);
    console.log(real_tastes);
    
    return new Pofin(real_tastes,this.getSmooth());
 }
 
 getSmooth(){
 
   let accordition_time_selection=document.querySelector("select[name='accordition']");
   
   if(this.used_nuts_name.length===1){
     accordition_time_selection.selectedIndex=0;
     return this.smooth_sum-1;
   }
   
   let all_smooth=parseInt(Math.ceil(this.smooth_sum/this.used_nuts_name.length));
   
   let selected_index=accordition_time_selection.options.selectedIndex;
   
   
   let bounus=parseInt(accordition_time_selection.options[selected_index].value);
   
   let smooth_result=all_smooth-this.used_nuts_name.length-bounus;
   
   if(smooth_result < 1){
     smooth_result=1;
   }
   
   return smooth_result;
   
 }
 
 toString(){
   
   let used_nutses=this.used_nuts_name[0];
   for(var i=1;i<this.used_nuts_name.length;i++){
     used_nutses=used_nutses+"+"+this.used_nuts_name[i];
   }
   return used_nutses;
 }
 
 static isOverlapNuts(all_nuts){
   return all_nuts.length !== new Set(all_nuts).size;
 }
 
 
}
  
  
    
   