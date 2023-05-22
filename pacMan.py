var scores;
$(document).ready(function()
{
	$.getJSON("../static/Json/Scores.json", function(result)
	{
		scores = JSON.parse(JSON.stringify(result));
		fillHighScores(scores);
	});
});

//Fill Highscore table from JSON file
function fillHighScores(scores)
{
	let scoresTable = document.getElementById("highScoresTable");

	for (i in scores.scores)
	{
		const name = scores.scores[i].Name;
		const Score = scores.scores[i].Score;

		//Create row
		var entry = scoresTable.insertRow();

		//Create Cells
		var nameEntry = entry.insertCell(0);
		var ScoreEntry = entry.insertCell(1);

		//Append text to cell
		let newName = document.createTextNode(name);
		nameEntry.appendChild(newName);
		let newScore = document.createTextNode(Score);
		ScoreEntry.appendChild(newScore);
	}
}


//If we have won a pacMan game let the user add their name to the score if it is a high score by enabling the high score submit button
if (window.location.href.indexOf("?") > -1)
{
	let startButton = document.getElementById("startButton");
	startButton.disabled = true;
	let highScoreNameInput = document.getElementById("highScoreNameInput");
	highScoreNameInput.disabled = false;
	let highScoreSubmitButton = document.getElementById("highScoreSubmitButton");
	highScoreSubmitButton.disabled = false;
}

//Sprite Objects
var pacManObj = null;
var Pinky = null;
var Blinky = null;
var Inky = null;
var Clyde = null;

//audio
var audio = new Audio("../static/audio/pacman_beginning.wav");
audio.muted = true;

//Map Object
var moveInformation = {
	//28 by 31 start at [23, 15]
	/*
	0 is wall
	1 is pellet
	2 is big pellet
	3 is eaten
	*/
	map: [
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], //0
		[0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
		[0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
		[0, 2, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2, 0],
		[0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
		[0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0], //5
		[0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0],
		[0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0],
		[0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0],
		[0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0], //10
		[0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, -1, -1, -1, -1, -1, -1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, -1, -1, -1, -1, -1, -1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
		[0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, -1, -1, -1, -1, -1, -1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
		[0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, -1, -1, -1, -1, -1, -1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0], //15
		[0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
		[0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0], //20
		[0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
		[0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
		[0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0], //23
		[0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0],
		[0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0], //25
		[0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0],
		[0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0],
		[0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
		[0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] //30
	],
	//If the Ghosts are moving
	PinkyInterval: 0,
	BlinkyInterval: 0,
	InkyInterval: 0,
	ClydeInterval: 0,
	//if blue mode is active
	blueMode: 0
};

//Constructor for pacMan
function Sprite(spriteName, location, left, top, direction)
{
	this.img = document.getElementById(spriteName);
	this.location = location;
	this.img.style.left = left;
	this.img.style.top = top;
	this.direction = direction;
}

//Constructor for Ghosts
function Ghost(spriteName, location, left, top, direction)
{
	this.img = document.getElementById(spriteName);
	this.name = spriteName;
	this.location = location;
	this.img.style.left = left;
	this.img.style.top = top;
	this.direction = direction;
	this.caneatpacMan = true;
}

//Initialize Game
function init()
{
	document.getElementById("startButton").disabled = true;
	//Inititialze pellets
	fill();

	//Initialize ghosts
	Pinky = new Ghost("Pinky", [11, 16], "44.2%", "33.5%", "none");
	Blinky = new Ghost("Blinky", [11, 11], "22%", "33.5%", "left");
	Inky = new Ghost("Inky", [17, 16], "32.3%", "53.2%", "left");
	Clyde = new Ghost("Clyde", [17, 11], "10%", "53.2%", "right");

	//Initialize pacMan
	pacManObj = new Sprite("pacManObj", [23, 15], "46.5%", "72%", "left");

	//Display Sprites
	pacManObj.img.style.visibility = 'visible';
	Pinky.img.style.visibility = 'visible';
	Blinky.img.style.visibility = 'visible';
	Inky.img.style.visibility = 'visible';
	Clyde.img.style.visibility = 'visible';

	audio.muted = false;
	audio.play();
	setTimeout(() =>
	{
		init2(pacManObj, Pinky, Blinky, Inky, Clyde);
	}, 4020);
}

//Initializes controls and starts the game
function init2(pacManObj, Pinky, Blinky, Inky, Clyde)
{

	//Initialize keyboard event listener
	//Enable player controlled movement
	audio.src = ("../static/audio/pacman_chomp.wav");
	document.getElementById("start").style.visibility = "hidden";
	document.addEventListener("keydown", (event) =>
	{
		switch (event.key)
		{
			case 'w': //MoveUp
				pacManObj.direction = 'up';
				break;
			case 's': //MoveDown
				pacManObj.direction = 'down';
				break;
			case 'd': //MoveRight
				pacManObj.direction = 'right';
				break;
			case 'a': //MoveLeft
				pacManObj.direction = 'left';
				break;
		}
	}, false);

	//Set interval to change pacman design
	setInterval(function()
	{
		change();
	}, 75);

	//set interval to move pacman
	setInterval(function()
	{
		move();
	}, 110);

	moveInformation.PinkyInterval = setInterval(function()
	{
		GhostMove(Pinky);
	}, 110);
	moveInformation.BlinkyInterval = setInterval(function()
	{
		GhostMove(Blinky);
	}, 110);
	moveInformation.InkyInterval = setInterval(function()
	{
		GhostMove(Inky);
	}, 110);
	moveInformation.ClydeInterval = setInterval(function()
	{
		GhostMove(Clyde);
	}, 110);

	//Timer
	setInterval(function()
	{
		Timer();
	}, 1000);
}

//timer
function Timer()
{
	let seconds = document.getElementById("secondNumber");
	let numSeconds = parseInt(seconds.innerHTML);
	if (numSeconds == 59)
	{
		let minutes = document.getElementById("minuteNumber");
		minutes.innerHTML = parseInt(minutes.innerHTML) + 1;
		seconds.innerHTML = "00";
	}
	else
	{
		if (numSeconds < 10)
		{
			seconds.innerHTML = "0" + (parseInt(seconds.innerHTML) + 1);
		}
		else
		{
			seconds.innerHTML = parseInt(seconds.innerHTML) + 1;
		}

	}
}

//Animates Pacman
function change()
{
	if (pacManObj.img.getAttribute('src') == "../static/images/pacMan.png")
	{
		switch (pacManObj.direction)
		{
			case 'up':
				pacManObj.img.style.transform = 'rotate(270deg)';
				break;
			case 'down':
				pacManObj.img.style.transform = 'rotate(90deg)';
				break;
			case 'left':
				pacManObj.img.style.transform = 'rotate(180deg)';
				break;
			case 'right':
				pacManObj.img.style.transform = 'rotate(0deg)'
				break;
		}

		pacManObj.img.src = "../static/images/pacManOpen.png";

	}
	else
	{
		pacManObj.img.src = "../static/images/pacMan.png";
	}


}

//Decide in which direction the ghost will move/ contains the Ghost AI
//Helper functions:pacManGhostCollisionHandle, moveInNewDirection
function GhostMove(Ghost)
{
	//Check to see if we are currently in the same space as Pacman
	pacManGhostCollisionHandle(Ghost);

	//We don't want ghosts always just moving forwards in a straight line this behavior is too predictable so we introduce a chance to at any moment move randomly in a new direction
	let randomlyMove = Math.floor(Math.random() * 3);

	if (randomlyMove != 0)
	{
		let continuedToMoveInDirection = 0;
		//Check to see if we can continue to move in the same direction
		switch (Ghost.direction)
		{
			case ("down"):
				continuedToMoveInDirection = GhostMoveDown(Ghost);
				break;
			case ("up"):
				continuedToMoveInDirection = GhostMoveUp(Ghost);
				break;
			case ("right"):
				continuedToMoveInDirection = GhostMoveRight(Ghost);
				break;
			case ("left"):
				continuedToMoveInDirection = GhostMoveLeft(Ghost);
				break;
		}

		//change directions if we cant move in the same direction
		if (continuedToMoveInDirection == 0)
		{
			ghostMoveInNewDirection(Ghost);
		}
	}
	//Randomly Move in a new direction
	else
	{
		ghostMoveInNewDirection(Ghost);
	}

	//Check to see if we have moved into the same space as Pacman
	pacManGhostCollisionHandle(Ghost);
}

//Randomly Move in a new direction
//Helper functions: getPossibleGhostDirections
function ghostMoveInNewDirection(Ghost)
{

	//Create an array of all possible direction to move except for the direction we already are moving in
	let possibleDirectionToMove = getPossibleGhostDirections(Ghost);
	let randomNum = Math.floor(Math.random() * possibleDirectionToMove.length);

	switch (possibleDirectionToMove[randomNum])
	{
		case "down":
			GhostMoveDown(Ghost);
			Ghost.direction = "down";
			break;
		case "up":
			GhostMoveUp(Ghost);
			Ghost.direction = "up";
			break;
		case "right":
			GhostMoveRight(Ghost);
			Ghost.direction = "right";
			break;
		case "left":
			GhostMoveLeft(Ghost);
			Ghost.direction = "left";
			break;
	}


}

//Get all possible directions that the Ghost can move into because we want the ghost to always move forward we remove the inverse direction it is currently moving in
function getPossibleGhostDirections(Ghost)
{
	let possibleDirectionToMove = [];

	//up
	if ((moveInformation.map[Ghost.location[0] - 1][Ghost.location[1]] != 0) && Ghost.direction != "down")
	{
		possibleDirectionToMove.push("up");
	}
	//down
	if ((moveInformation.map[Ghost.location[0] + 1][Ghost.location[1]] != 0) && Ghost.direction != "up")
	{
		possibleDirectionToMove.push("down");
	}
	//left
	if ((moveInformation.map[Ghost.location[0]][Ghost.location[1] - 1] != 0) && Ghost.direction != "right")
	{
		possibleDirectionToMove.push("left");
	}
	//right
	if ((moveInformation.map[Ghost.location[0]][Ghost.location[1] + 1] != 0) && Ghost.direction != "left")
	{
		possibleDirectionToMove.push("right");
	}
	//If we can only move backwards
	if (possibleDirectionToMove.length == 0)
	{
		switch (Ghost.direction)
		{
			case "down":
				Ghost.direction = "up";
				break;
			case "up":
				Ghost.direction = "down";
				break;
			case "right":
				Ghost.direction = "left";
				break;
			case "left":
				Ghost.direction = "right";
				break;
		}
		possibleDirectionToMove.push(Ghost.direction);
	}

	return possibleDirectionToMove;
}

//Move Ghost up
function GhostMoveUp(Ghost)
{
	//move up if possible
	if (moveInformation.map[Ghost.location[0] - 1][Ghost.location[1]] != 0)
	{
		Ghost.img.style.top = parseFloat(Ghost.img.style.top) - 3.2 + "%";
		Ghost.location[0]--;
		return 1;
	}
	return 0;
}

//Move Ghost down
function GhostMoveDown(Ghost)
{
	//move down if possible
	if (moveInformation.map[Ghost.location[0] + 1][Ghost.location[1]] != 0)
	{
		Ghost.img.style.top = parseFloat(Ghost.img.style.top) + 3.2 + "%";
		Ghost.location[0]++;
		return 1;
	}
	return 0;
}

//Move Ghost left
function GhostMoveLeft(Ghost)
{
	//move left if possible
	if (moveInformation.map[Ghost.location[0]][Ghost.location[1] - 1] != 0)
	{
		Ghost.img.style.left = parseFloat(Ghost.img.style.left) - 3.2 + "%";
		Ghost.location[1]--;
		return 1;
	}
	return 0;
}

//Move Ghost right
function GhostMoveRight(Ghost)
{
	//move right if possible
	if (moveInformation.map[Ghost.location[0]][Ghost.location[1] + 1] != 0)
	{
		Ghost.img.style.left = parseFloat(Ghost.img.style.left) + 3.2 + "%";
		Ghost.location[1]++;
		return 1; //bruh
	}
	return 0;
}

//Pinky Ai move
//Follow the player
/*Not used
function PinkyMove()
{

    //move down
    if(((Pinky.location[0] - pacManObj.location[0]) < 0))
    {
        GhostMoveDown(Pinky);

    }

        //move up
        if(((Pinky.location[0] - pacManObj.location[0]) > 0))
    {
        GhostMoveUp(Pinky);
    }

        //move left
        if(((Pinky.location[1] - pacManObj.location[1]) > 0))
    {
        GhostMoveLeft(Pinky);
    }

        //move right
        if(((Pinky.location[1] - pacManObj.location[1]) < 0))
    {
        GhostMoveRight(Pinky);
    }
    pacManGhostCollisionHandle(Pinky);

}
*/

//Determine if and what to do in the event a ghost and pacman collide
function pacManGhostCollisionHandle(CurrentGhost)
{

	if (JSON.stringify(CurrentGhost.location) === JSON.stringify(pacManObj.location))
	{
		if (CurrentGhost.caneatpacMan == true)
		{
			window.location.reload();
		}
		else
		{
			document.getElementById("scoreNumber").innerHTML = parseInt(document.getElementById("scoreNumber").innerHTML) + 50;
			respawnGhost(CurrentGhost);
		}
	}

}

//Moves Pacman
function move()
{
	switch (pacManObj.direction)
	{
		case 'up': //MoveUp
			moveHelper([-1, 'y', -3.2]);
			break;

		case 'down': //MoveDown
			moveHelper([1, 'y', 3.2]);
			break;

		case 'right': //MoveRight
			moveHelper([1, 'x', 3.2]);
			break;

		case 'left': //MoveLeft
			moveHelper([-1, 'x', -3.2]);
			break;

	}
}

//Helper function to move Pacman
function moveHelper(PacManMoveParameters)
{

	//Move in the y direction
	if (PacManMoveParameters[1] == 'y')
	{
		//move
		if (moveInformation.map[pacManObj.location[0] + PacManMoveParameters[0]][pacManObj.location[1]] > 0)
		{
			pacManObj.img.style.top = parseFloat(pacManObj.img.style.top) + PacManMoveParameters[2] + "%";
			pacManObj.location[0] = pacManObj.location[0] + PacManMoveParameters[0];
		}
	}

	//Move in the x direction
	else
	{
		//move
		if (moveInformation.map[pacManObj.location[0]][pacManObj.location[1] + PacManMoveParameters[0]] > 0)
		{
			pacManObj.img.style.left = parseFloat(pacManObj.img.style.left) + PacManMoveParameters[2] + "%";
			pacManObj.location[1] = pacManObj.location[1] + PacManMoveParameters[0];
		}
	}
	//Remove pellet if needed
	if (moveInformation.map[pacManObj.location[0]][pacManObj.location[1]] != 3)
	{
		removePellet();
	}
}

//Removes the Pellet at the location PacMan moves into
//Contains the win condition
function removePellet()
{
	//Remove the pellet and increase score by 10
	const imageToBeRemoved = document.getElementById(pacManObj.location[0] + '!' + (pacManObj.location[1]));
	document.getElementById("pacManDiv").removeChild(imageToBeRemoved);
	document.getElementById("scoreNumber").innerHTML = parseInt(document.getElementById("scoreNumber").innerHTML) + 10;
	audio.play();

	//If the Pellet eaten was a big pellet activate Blue Ghost mode
	if (moveInformation.map[pacManObj.location[0]][pacManObj.location[1]] == 2)
	{
		PacManBlueMode();
	}

	moveInformation.map[pacManObj.location[0]][pacManObj.location[1]] = 3;

	//If all pellets have been eaten win the game
	if (document.getElementById("pacManDiv").childNodes.length == 13)
	{
		//When we beat the game check to see if we have a high score
		$.getJSON("../static/Json/Scores.json", function(result)
		{
			const scores = JSON.parse(JSON.stringify(result));
			let currentPlayerscore = parseInt(document.getElementById("scoreNumber").innerHTML);
			//If the player score is lower than all current highscores we do not update the highscore JSON
			if ((scores.scores[4].Score < currentPlayerscore))
			{
				EnableHighScoreInputPage(currentPlayerscore);
			}
		});
	}
}

//Reload Webpage with highscore input enabled
function EnableHighScoreInputPage(currentPlayerscore)
{
	//Reload url with score
	let url = window.location.href;
	url += "?score=" + currentPlayerscore;
	window.location.href = url;
}

//Respawn the eaten Ghost at the middle of the screen
function respawnGhost(Ghost)
{

	Ghost.img.style.visibility = "hidden";
	let leftTochange = "";
	let topTochange = "";
	switch (Ghost.name)
	{
		case "Pinky":
			clearInterval(moveInformation.PinkyInterval);
			leftTochange = "44.2%"
			topTochange = "40%"
			Ghost.location = [13, 16]
			break;
		case "Blinky":
			clearInterval(moveInformation.BlinkyInterval);
			leftTochange = "22%"
			topTochange = "40%"
			Ghost.location = [13, 11]
			break;
		case "Inky":
			clearInterval(moveInformation.InkyInterval);
			leftTochange = "32.3%"
			topTochange = "46.7%"
			Ghost.location = [15, 16]
			break;
		case "Clyde":
			clearInterval(moveInformation.ClydeInterval);
			leftTochange = "11%"
			topTochange = "46.7%"
			Ghost.location = [15, 11]
			break;
	}
	setTimeout(() =>
	{
		restartGhost(Ghost);
	}, 3300);
	Ghost.img.style.left = leftTochange;
	Ghost.img.style.top = topTochange;
}

//Restart the Ghost moving cycle
function restartGhost(Ghost)
{

	Ghost.img.src = ("../static/images/" + Ghost.name + ".png");
	Ghost.img.style.visibility = "visible";
	Ghost.direction = 'up';
	Ghost.caneatpacMan = true;

	switch (Ghost.name)
	{
		case "Pinky":
			moveInformation.PinkyInterval = setInterval(function()
			{
				GhostMove(Pinky)
			}, 110);
			break;
		case "Blinky":
			moveInformation.BlinkyInterval = setInterval(function()
			{
				GhostMove(Blinky)
			}, 110);
			break;
		case "Inky":
			moveInformation.InkyInterval = setInterval(function()
			{
				GhostMove(Inky)
			}, 110);
			break;
		case "Clyde":
			moveInformation.ClydeInterval = setInterval(function()
			{
				GhostMove(Clyde)
			}, 110);
			break;
	}

}

//Starts BlueMode that allows pacMan to eat ghosts
function PacManBlueMode()
{

	if (moveInformation.blueMode == 0)
	{
		moveInformation.blueMode = 1;

		Pinky.img.src = "../static/images/BlueGhost.png";
		Blinky.img.src = "../static/images/BlueGhost.png";
		Inky.img.src = "../static/images/BlueGhost.png";
		Clyde.img.src = "../static/images/BlueGhost.png";

		Pinky.caneatpacMan = false;
		Blinky.caneatpacMan = false;
		Inky.caneatpacMan = false;
		Clyde.caneatpacMan = false;
		//500 Cycles
		setTimeout(() =>
		{
			PacManReturnToNormalMode();
		}, 5500);
	}
}

//end Blue mode
function PacManReturnToNormalMode()
{
	Pinky.img.src = "../static/images/Pinky.png";
	Blinky.img.src = "../static/images/Blinky.png";
	Inky.img.src = "../static/images/Inky.png";
	Clyde.img.src = "../static/images/Clyde.png";

	Pinky.caneatpacMan = true;
	Blinky.caneatpacMan = true;
	Inky.caneatpacMan = true;
	Clyde.caneatpacMan = true;

	moveInformation.blueMode = 0;
}

//Fill with Pellets
//Helper function: addPellet
function fill()
{

	for (var y = 0; y < moveInformation.map.length; y++)
	{
		for (var x = 0; x < moveInformation.map[0].length; x++)
		{
			let pelletPotential = moveInformation.map[y][x];
			if (pelletPotential != 0)
			{
				switch (pelletPotential)
				{
					case 1:
						addPellet(y, x, "Pellet");
						break;
					case 2:
						addPellet(y, x, "BigPellet");
						break;
				}
			}

		}
	}

}

//Create and add the pellets to the document
function addPellet(y, x, size)
{
	const image = document.createElement('img');
	image.src = "../static/images/" + size + ".png";
	image.id = y + '!' + x;
	image.style.position = "fixed";
	image.style.left = (x + .5) * 16 + 'px';
	image.style.top = (y + 3.5) * 16 + 'px';
	const element = document.getElementById("pacManDiv");
	element.appendChild(image);
}

//Mutes and Unmutes
function Mute()
{
	audio.muted = !audio.muted;
}

//Update scores JSON with a new high score
function updateScores()
{
	let highScoreNameInput = document.getElementById("highScoreNameInput");
	let nameInput = highScoreNameInput.value;
	highScoreNameInput.value = "";
	highScoreNameInput.disabled = true;
    nameInput = String(nameInput)
    if(nameInput.length > 0 && nameInput.length < 10)
    {
	//If the user doesn't input a special character we update the scores
	if (nameInput.search(/[^A-Za-z0-9]/) == -1)
	{
        const urlParams = new URLSearchParams(window.location.search);
        let currentPlayerscore = urlParams.get('score');

		let newScoreLocation = getNewScoreLocation(currentPlayerscore);

		highScoreNameInput.disabled = true;

		$.ajax(
		{
			url: "/pacManUpdateScores",
			type: "POST",
			data:
			{
				name: nameInput,
				score: currentPlayerscore,
				loc: newScoreLocation
			}
		});
	}
	else
	{
		alert("special characters are not allowed");
		highScoreNameInput.disabled = false;
	}
    }
    else
    {
        alert("Invalid name length must be between 1 and 10 characters");
        highScoreNameInput.disabled = false;
    }
}

//get The location to insert the high score into by find which scores are lower than the current player score
function getNewScoreLocation(currentPlayerscore)
{
    //Find the location for highscore insertion
	for (let i = 4; i >= 0; i--)
	{
		if (currentPlayerscore < Number(scores.scores[i].Score))
		{
            return (i+1);
		}
	}
	return 0;
}
