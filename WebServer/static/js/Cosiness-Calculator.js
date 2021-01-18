// Coloring Values of tempreture , humidity , co2 ... 
window.onload = function(){

    // get AHP value from server for this room

    var ahpvalueroom = document.getElementById("value").innerHTML ; 
    

    if( ahpvalueroom >= 0 && ahpvalueroom <= 39 ){


        document.getElementById("iscosy").innerHTML = "Not Cosy";
        document.getElementById('emoji').src="../static/images/sad.png";  

    } else if (ahpvalueroom >= 40 && ahpvalueroom <= 69) {

        document.getElementById("iscosy").innerHTML = "Mid Cosy";
        document.getElementById('emoji').src="../static/images/meh.png";  
 
    } else if (ahpvalueroom >= 70 && ahpvalueroom <= 100) {

        document.getElementById("iscosy").innerHTML = "Really Cosy";
        document.getElementById('emoji').src="../static/images/smile.png";  

    }

var tempreture = document.getElementById("one").innerHTML

if( tempreture >= 16 && tempreture <= 22 ){
 
    document.getElementById("oneone").style.backgroundColor = "green" ;  

}
else if ( (tempreture >= 13 && tempreture <= 15 )|| (tempreture >= 23 && tempreture <= 26) ) {

    document.getElementById("oneone").style.backgroundColor = "yellow" ;  

}

else {
  
    document.getElementById("oneone").style.backgroundColor = "red" ;  
}

 var soundlevel = document.getElementById("two").innerHTML

if( soundlevel >= 0 && soundlevel < 600 ){
    // document.getElementById("Tempreture").value = "Cange Color green"
    
    document.getElementById("twotwo").style.backgroundColor = "green" ;  


}
else if( soundlevel >= 600 && soundlevel < 800 ){
    
    document.getElementById("twotwo").style.backgroundColor = "yellow" ;  


}

else {
    document.getElementById("twotwo").style.backgroundColor = "red" ;  


}

var lightLevel = document.getElementById("three").innerHTML

if( lightLevel > 200 && lightLevel < 500 ){
    // document.getElementById("Tempreture").value = "Cange Color green"
    
    document.getElementById("threethree").style.backgroundColor = "green" ;  


}

else if( (lightLevel >= 50 && lightLevel <= 200 )|| (lightLevel >= 500 && lightLevel < 1000)  ){
    
    document.getElementById("threethree").style.backgroundColor = "yellow" ;  


}

else if (lightLevel >= 100){
    document.getElementById("threethree").style.backgroundColor = "red" ;  


}

var Humaditylevel = document.getElementById("four").innerHTML

if( Humaditylevel > 30 && Humaditylevel < 60 ){
    
    document.getElementById("fourfour").style.backgroundColor = "green" ;  


}

else if( (Humaditylevel >= 25 && Humaditylevel <= 30) || (Humaditylevel >= 60 && Humaditylevel <= 70)  ){
    
    document.getElementById("fourfour").style.backgroundColor = "yellow" ;  


}

else {

    document.getElementById("fourfour").style.backgroundColor = "red" ;  


}

//  Calculate C02 

var co2Level = document.getElementById("five").innerHTML

if( co2Level > 0 && co2Level < 800 ){
    
    document.getElementById("fivefive").style.backgroundColor = "green" ;  


}

else if( (co2Level >= 800 && co2Level <= 2000)  ){
    
    document.getElementById("fivefive").style.backgroundColor = "yellow" ;  


}

else if (co2Level > 2000){

    document.getElementById("fivefive").style.backgroundColor = "red" ;  


}
}