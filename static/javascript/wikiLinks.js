function checkTwitter()
{
  alert("boo")
  canvas = RefreshCanvas();
  Input = document.getElementById("Input");
  searchTopic = Input.value;
  Input.value = '';

    $.ajax({
  url: "/wikiLinksProcess",
  type: "POST",
  data: { 
            searchRequest: searchTopic
        },
}).done(function(jsonWikiLinks)
  {
    const parsedWikiLinks = JSON.parse(jsonWikiLinks);

   let parsedWikiLinksvalues = Object.keys(parsedWikiLinks);
   let parsedWikiLinksKeys = Object.values(parsedWikiLinks);


    new Chart(canvas, {
      type: "pie",
      data: {
        labels: parsedWikiLinksKeys,
        datasets: [{
          backgroundColor: barColors,
          data: parsedWikiLinksvalues
        }]
      },
      options: {
        title: {
          display: true,
          text: "Wiki Links"
        }
      }
    });

  });

}

//Calls: None
//Destroy the current Canvas and replace it with a new one
function RefreshCanvas()
{
  //Create A New Canvas 
  var CanvasToBeDestroyed = document.getElementById("wikiCanvas");
  CanvasToBeDestroyed.remove();
  var Container = document.getElementById("wikichartContainer");
  var canvas = document.createElement("wikiCanvas");
  canvas.className = "wikiCanvas"
  canvas.id = "wikiCanvas"
  alert("hfdselo")
  Container.appendChild(canvas)
  alert("he46lo")
  return(canvas)
}