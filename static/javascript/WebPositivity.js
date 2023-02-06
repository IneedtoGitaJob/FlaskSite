
//Calls: None
//Fills a load bar arbitrarily, the load bar isn't actually related to progress and is instead a way to show the user that the website is still working 
function LoadBar(loadBarTimeInterval)
{

  document.getElementById("submitButton").disabled = true;
  var id;
  var i = 0
  if (i == 0) {
    i = 1;
    var elem = document.getElementById("Bar");
    var width = 1;
    id = setInterval(frame, loadBarTimeInterval);
    function frame() {
      if (width >= 90) {
        clearInterval(id);
        i = 0;
      } else {
        width++;
        elem.style.width = width + "%";
      }
    }
  }

  $(document).ajaxStop(
    
    function(){
      clearInterval(id);
      var elem = document.getElementById("Bar");
      elem.style.width = "100%";
      document.getElementById("submitButton").disabled = false;
    });

}

//Calls: RefreshCanvas, backgroundWebProcess
//Checks a website for positivity and sets a color to match the positivity
function checkWeb(TextInput) 
{
  canvas = RefreshCanvas();

  $(document).ajaxStart(LoadBar(40));

    $.ajax({
  url: '/backgroundWebProcess',
  type: "POST",
  data: { 
          text: TextInput
        },
}).done(function( o ) {

    //Failed to connect
    if(o == "Fail")
    {
        alert("Failed to connect Improper request")
    }
    else
    {

        //Fill Canvas
        var ctx = canvas.getContext('2d');
        ctx.fillStyle = o;
        ctx.fillRect(0,0,canvas.width, canvas.height);


    }

});

}

//Calls: RefreshCanvas, backgroundNewsProcessMulti
//Checks Years of News Stories and returns a pie chart of the average positivity
function checkManyWebs(TextInput, yearsInput)
{

  canvas = RefreshCanvas();

  $(document).ajaxStart(LoadBar(200));

    //Get a String of News positivity
    $.ajax({
  url: "/backgroundNewsProcessMulti",
  type: "POST",
  data: { 
          text: TextInput,
          Years: yearsInput
        },
}).done(function( o ) {


if(o != "Fail")
{

var xValues = ["Very Positive", "Positive", "Neutral", "Negative", "Very Negative"];

//Parse the String into an Integer Array
var RawValues = o.split(' ').map(function(item) {
    return parseInt(item, 10);
});
//alert(RawValues)
var yValues = [0,0,0,0,0];

RawValues.forEach(function(x){

//Very Positive
if(x >= 80)
{
    yValues[0]++;
}
else
{
//Positive
if(x >= 60 && x < 80)
{
yValues[1]++;
}
else
{
//Neutral
if(x >= 40 && x < 60)
{
yValues[2]++;
}
else
{
//Negative
if(x < 40 && x >= 20)
{
yValues[3]++;
}
//VeryNegative
else
{
yValues[4]++;  
}
}
}
}

});

var barColors = [
  "#00ff00",
  "#00aa00",
  "#ffff00",
  "#aa0000",
  "#ff0000"
];

//Create chart
new Chart(canvas, {
  type: "pie",
  id: "Pie Chart",
  data: {
    labels: xValues,
    datasets: [{
      backgroundColor: barColors,
      data: yValues
    }]
  },
  options: {
    maintainAspectRatio: false,
    title: {
      display: true,
      text: "Average News Positivity"
    }
  }
});

}
else
{
    alert("Search Failed")
}


    
});
}

function checkTwitter(TextInput, yearsInput)
{
  canvas = RefreshCanvas();
  $(document).ajaxStart(LoadBar(200));

    $.ajax({
  url: "/twitterProcess",
  type: "POST",
  data: { 
          text: TextInput,
          Years: yearsInput
        },
}).done(function(sentimentTotalForEachYear)
  {

if(sentimentTotalForEachYear.length > 0)
{
  let currentYear = Number(currentTime.getFullYear())
  //Fill years 
  //change sentimentTotalForEachYear to a dict as we are accessing current year at too many different times
  let xValues = []
  for(let x = currentYear-yearsInput ; x <=currentYear;x++)
  {
    xValues.push(x);
  }

  new Chart(canvas, {
    type: "line",
    id: "Line Chart",
    data: {
      labels: xValues,
      datasets: [{
        backgroundColor: "rgba(0,0,0,1.0)",
        borderColor: "rgba(0,0,0,0.1)",
        data: sentimentTotalForEachYear
      }]
      },
    options: {
      maintainAspectRatio: false,
      title: {
        display: true,
        text: "Average Twitter Positivity"
      }
    }
  });

}
else{alert("Request Failed")}

  });

}


//Calls: checkManyWebs or checkWeb, VerifyYears
//Takes and verifies user input then calls checkManyWebs or checkWeb
function executeFunction() 
{

    //Store inputs and check for valid inputs
    var TextInput = document.getElementById("Input").value;
    var RadioInput = document.querySelector('input[name="rad"]:checked').id
    var yearsInput = document.getElementById("yearsInput").value;

    //Clear inputs
    document.getElementById("Input").value = '';
    document.getElementById("yearsInput").value = '';

    //Use Inputs
        if(TextInput == "")
        {
            alert("No Input given")
        }
        else
        {
          switch(RadioInput)
          {
            case "":
              alert("No Selection given")
              break;
            case "Website":
              checkWeb(TextInput);
              break;
            case "Tweets":
              checkTwitter(TextInput, yearsInput);
              break;
            case "News":
              checkManyWebs(TextInput, yearsInput);
              break;
          }
        }
      
        }

//Calls:None
//Verify that the given years is a number that is within the timerange 2004-currentyear
function VerifyYears(yearsInput)
{
    var currentYear = new Date().getFullYear() ;
    if(Number.isInteger(Number(yearsInput)) && (yearsInput != 0) &&  ((currentYear - 2004) >= yearsInput))
    {
        return(true)
    }
    else
    {
        return(false)
    }
 
}

//Calls: None
//Destroy the current Canvas and replace it with a new one
function RefreshCanvas()
{

  //Create A New Canvas 
  var CanvasToBeDestroyed = document.getElementById("Canvas");
  CanvasToBeDestroyed.remove();
  var Container = document.getElementById("Container");
  var canvas = document.createElement("Canvas");
  canvas.className = "Canvas"
  canvas.id = "Canvas"
  Container.appendChild(canvas)
  return(canvas)
}
