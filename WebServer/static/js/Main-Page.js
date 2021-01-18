window.onload = function(){

    // Coloring Rooms in main Page

    var ahpvalueroom1 = document.getElementById("value1").innerText;

    // color for room 1 in main page
    // ROOOOOOOOOOOOOOOOOOOOOOOOOM 1 Coloring the main page room 1 
    
    if( ahpvalueroom1 >= 0 && ahpvalueroom1 <= 39 ){
        
        document.getElementById("room1color").style.backgroundColor = "red" ;

    } else if (ahpvalueroom1 >= 40 && ahpvalueroom1 <= 69) {

        document.getElementById("room1color").style.backgroundColor = "yellow" ;

 
    } else if (ahpvalueroom1 >= 70 && ahpvalueroom1 <= 100) {

        document.getElementById("room1color").style.backgroundColor = "green" ;
    }

    var ahpvalueroom2 = document.getElementById("value2").innerText;

   // color for room 2 in main page
    // ROOOOOOOOOOOOOOOOOOOOOOOOOM 2 Coloring the main page room 1 
    
    if( ahpvalueroom2 >= 0 && ahpvalueroom2 <= 39){
        
        document.getElementById("room2color").style.backgroundColor = "red" ;

    } else if (ahpvalueroom2 >= 40 && ahpvalueroom2 <= 69) {

        document.getElementById("room2color").style.backgroundColor = "yellow" ;

 
    } else if (ahpvalueroom2 >= 70 && ahpvalueroom2 <= 100) {

        document.getElementById("room2color").style.backgroundColor = "green" ;
    }

    var ahpvalueroom3 = document.getElementById("value3").innerText;

   // color for room 1 in main page
    // ROOOOOOOOOOOOOOOOOOOOOOOOOM 2 Coloring the main page room 2 
    
    if( ahpvalueroom3 >= 0 && ahpvalueroom3 <= 39){
        
        document.getElementById("room3color").style.backgroundColor = "red" ;

    } else if (ahpvalueroom3 >= 40 && ahpvalueroom3 <= 69) {

        document.getElementById("room3color").style.backgroundColor = "yellow" ;

 
    } else if (ahpvalueroom3 >= 70 && ahpvalueroom3 <= 100) {

        document.getElementById("room3color").style.backgroundColor = "green" ;
    }

}




