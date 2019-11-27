var egypt = true;
$("#eg").prop("checked", true);

//Toggle Maps
$("#maps img").on("click", event=>{
  var el = event.target;
  if(!$(el).hasClass("selected")){
    $("#maps img").removeClass("selected");
    $(el).addClass("selected");
    egypt = !egypt;

    if(egypt){
      $("#eg").prop("checked", true);
      $("#us").prop("checked", false);
    }
    else{
      $("#eg").prop("checked", false);
      $("#us").prop("checked", true);
    }
  }

  $("button").on("click", event=>{
    if(!validateInput()){
      event.preventDefault();
      alert("You need to choose both agents");
    }
    else{
      var map = "egypt";
      var agentOneType = $("#playerOne").val();
      var agentTwoType = $("#playerTwo").val();
      console.log(agentOne);
      console.log(agentTwo);
      if(!egypt) {
          map = "usa";
      }
      var gameSettings = {
              mapName: map,
              agentOneType: agentOneType,
              agentOneName: "blue",
              agentTwoType: agentTwoType,
              agentTwoName: "red"
           }
    }
  });
})



//Helper Functions
function validateInput(){
  var p1 = $("#playerOne").val();
  var p2 = $("#playerTwo").val();
  if(p1!==null & p2!==null){return true;}
}