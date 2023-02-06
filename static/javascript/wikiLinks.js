//Get and Display wiki Links
function displayWikiLinks()
{

  //Get text input and reset
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
            //parse
            const parsedWikiLinks = JSON.parse(jsonWikiLinks);
            let parsedWikiLinksvalues = Object.keys(parsedWikiLinks);
            //let parsedWikiLinksKeys = Object.values(parsedWikiLinks);
            //Create the cyto object and display with links from parsed wikiLinks
            cyto(parsedWikiLinksvalues,searchTopic)
              
            });

}

function cyto(parsedWikiLinksvalues,searchTopic)
{
  var cy = cytoscape({

    container: document.getElementById('cy'), // container to render in
    
    elements: [
    ],
    
    style: [ // the stylesheet for the graph
      {
        selector: 'node',
        style: {
          'background-color': '#666',
          'label': 'data(id)'
        }
      },
    
      {
        selector: 'edge',
        style: {
          'width': 3,
          'line-color': '#ccc',
          'target-arrow-color': '#ccc',
          'target-arrow-shape': 'triangle',
          'curve-style': 'bezier'
        }
      }
    ],
    
    layout: {
      name: 'grid',
      rows: 1
    }
    
    });

    //Add the search term to the center of the graph
    cy.add({
      group: 'nodes',
      data: { id:searchTopic,weight: 75,height:100,width:100 },
      position: { x: 200, y: 200 }
  });

  //add all other links
    for(let x in parsedWikiLinksvalues)
    {
      cy.add({
        group: 'nodes',
        data: { id:parsedWikiLinksvalues[x],weight: 75 },
        position: { x: 200, y: 200 }
    });
    cy.add({
      group: 'edges',
      data: { id: (parsedWikiLinksvalues[x]+"edge"), source: parsedWikiLinksvalues[x], target: searchTopic },
      position: { x: 200, y: 200 }
  });
    }
    //set layout
    var layout = cy.layout({
      name: 'concentric'
    });
    
    layout.run();
}