//Get and Display wiki Links
function displayWikiLinks()
{

	//Get text input and reset
	Input = document.getElementById("Input");
	searchTopic = Input.value;
	Input.value = '';

	$.ajax(
	{
		url: "/wikiLinksProcess",
		type: "POST",
		data:
		{
			searchRequest: searchTopic
		},
	}).done(function(jsonWikiLinks)
	{

		//Check to see if the wiki links have been successfully retrieved
		const result = jsonWikiLinks.localeCompare(`"Fail"`);

		//If the wiki url isnt valid
		if (result != 0)
		{
			//parse
			const parsedWikiLinks = JSON.parse(jsonWikiLinks);
			let parsedWikiLinksvalues = Object.keys(parsedWikiLinks);
			let parsedWikiLinksKeys = Object.values(parsedWikiLinks);
			//Create the cyto object and display with links from parsed wikiLinks
			cyto(parsedWikiLinksvalues, parsedWikiLinksKeys, searchTopic)
		}
		else
		{
			alert("Search Not a valid wiki search")
		}
	});

}

//Create the cytoscape object
function cyto(parsedWikiLinksvalues, parsedWikiLinksKeys, searchTopic)
{
	var cy = cytoscape(
	{

		container: document.getElementById('cy'), // container to render in

		elements: [],

		style: [ // the stylesheet for the graph
			{
				selector: 'node',
				style:
				{
					'label': 'data(id)',
					'width': 'data(weight)',
					'height': 'data(weight)',
					'background-image': parsedWikiLinksKeys.pop()
				}
			},

			{
				selector: 'edge',
				style:
				{
					'width': 3,
					'line-color': '#ccc',
					'target-arrow-color': '#ccc',
					'target-arrow-shape': 'triangle',
					'curve-style': 'bezier'
				}
			}
		]
	});

	//Add the search term to the center of the graph
	cy.add(
	{
		group: 'nodes',
		data:
		{
			id: searchTopic,
			weight: 100,
			height: 100,
			width: 100
		}
	});

	//add all other links
	for (let x in parsedWikiLinksvalues)
	{
		cy.add(
		{
			group: 'nodes',
			data:
			{
				id: parsedWikiLinksvalues[x],
				weight: (parsedWikiLinksKeys[x] * 50)
			}
		});
		cy.add(
		{
			group: 'edges',
			data:
			{
				id: (parsedWikiLinksvalues[x] + "edge"),
				source: parsedWikiLinksvalues[x],
				target: searchTopic
			}
		});
	}
	//set layout
	var layout = cy.layout(
	{
		name: 'concentric'
	});

	layout.run();
}