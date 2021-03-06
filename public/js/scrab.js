let switchBehaviour=true

function toggleSwitch(item){
  if (switchBehaviour) {
    item.innerHTML="<h1>Tile Drop: Swap</h1>";
    switchBehaviour=false;
  } else {
    item.innerHTML="<h1>Tile Drop: Push</h1>";
    switchBehaviour=true;
  }
}

window.document.title="Scrabble Tile View"

function reorderTiles(sourceTile, targetTile) {
  let tiles = document.querySelector('#tiles');
  let tempTiles = [];
  let tileRegex = new RegExp('tile[1-7]');
  let calcNumbers={'1':1,'2':2,'3':3, '4':4, '5':5, '6':6, '7':7}

  sourceTilePassed=false
  targetTilePassed=false
  offset=0;

  if (switchBehaviour) {
    for (let i = 0; i < Object.keys(calcNumbers).length; i += 1) {
      if ((i+1) == parseInt(sourceTile.slice(-1))) {         // CLAUSE 1: Source tile
        sourceTilePassed=true                                // Set bool to mark source tile passed
        if (!targetTilePassed) {                             // In source tile clause and target tile not passed:
          calcNumbers[i+1]=i+2;                              //  apply positive offset (i+2) to shift tiles right
        } else {                                             // In source tile clause and target tile passed:
          calcNumbers[i+1]=i;                                //  apply negative offset (i) to shift tiles left
        }
      } else if ((i+1) == parseInt(targetTile.slice(-1))) {  // CLAUSE 2: Target tile
        targetTilePassed=true                                // Set bool to mark target tile passed
        calcNumbers[i+1]=(parseInt(sourceTile.slice(-1)));   // Target tile is always source tile integer
      } else if (sourceTilePassed==targetTilePassed) {       // CLAUSE 3: Neither source nor target passed OR both have passed:
          calcNumbers[i+1]=i+1;                              //  pass tile through unchanged
      } else if (sourceTilePassed) {                         // CLAUSE 4: Source tile passed but target not:
        calcNumbers[i+1]=i+2;                                //  apply positive offset (i+2) to shift tiles right
      } else if (targetTilePassed) {                         // CLAUSE 5: target tile passed but source not
        calcNumbers[i+1]=i;                                  //  apply negative offset (i) to shift tiles left
      }
    }
  } else {
    for (let i = 0; i < Object.keys(calcNumbers).length; i += 1) {
      if ((i+1) == parseInt(sourceTile.slice(-1))) {         // CLAUSE 1: Source tile
        calcNumbers[i+1]=(parseInt(targetTile.slice(-1)));   // Target tile is always source tile integer
      } else if ((i+1) == parseInt(targetTile.slice(-1))) {  // CLAUSE 2: Target tile
        calcNumbers[i+1]=(parseInt(sourceTile.slice(-1)));   // Source tile is always target tile integer
      } else {                                               // CLAUSE 3: Neither source nor target passed OR both have passed:
        calcNumbers[i+1]=i+1;                                //  pass tile through unchanged
      }
    }
  }

  for (let i = 0; i < tiles.children.length; i += 1) {
    tempTiles.push(tiles.children[calcNumbers[i+1]-1]);
  }
  while (tiles.children.length > 0) {
    tiles.removeChild(tiles.children[0]);
  }
  for (let i = 0; i < tempTiles.length; i += 1) {
    tempTiles[i].innerHTML = tempTiles[i].innerHTML.replace(tileRegex, "tile"+(i+1));
    tiles.appendChild(tempTiles[i]);
  }
  addHandlers();
}

function shuffleTiles() {
  let tiles = document.querySelector('#tiles');
  let tempTiles = [];
  let tileRegex = new RegExp('tile[1-7]');
  for (let i = 0; i < tiles.children.length; i += 1) {
    tempTiles.push(tiles.children[i]);
  }
  tempTiles.sort(function(a, b) {
    return -1 + Math.random() * 3;
  });
  while (tiles.children.length > 0) {
    tiles.removeChild(tiles.children[0]);
  }
  for (let i = 0; i < tempTiles.length; i += 1) {
    tempTiles[i].innerHTML = tempTiles[i].innerHTML.replace(tileRegex, "tile"+(i+1));
    tiles.appendChild(tempTiles[i]);
  }
  addHandlers()
}

let tileDragSrcEl = null;

function tileDragStart(e) {
  tileDragSrcEl = e.target;
  e
    .dataTransfer
    .setData('text', e.target.id);
}

function tileDragOver(e) {
  if (tileDragSrcEl) {
    e.preventDefault();
  }
}

function tileDrop(e) {
  if (tileDragSrcEl) {
    e.stopPropagation();
    e.stopImmediatePropagation();
    e.preventDefault();
    if (tileDragSrcEl != this) {
      let id = e
        .dataTransfer
        .getData('text');
      let sourceTile = document.getElementById(id);
      let targetTile = e.target;
      reorderTiles(sourceTile.id, targetTile.id)
    }
  }
}

function tileDragEnd(e) {
  tileDragSrcEl = null;
}

function updatePage() {
  location.reload();
}

function getParameterByName(name, url) {
    if (!url) url = window.location.href;
    name = name.replace(/[\[\]]/g, '\\$&');
    let regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)'),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, ' '));
}

async function fetchAsync () {
  let response = await fetch('https://8n831lmsk9.execute-api.eu-west-1.amazonaws.com/main/scrabState/'+getParameterByName("g")+'/'+getParameterByName("p"));
  let data = await response.json();
  return data;
}

fetchAsync()
    .then(
      data => {
        for (let i = 0; i < data.Items[0].tileRack.length; i++) {
          document.getElementById("tile"+(i+1)).src = 'img/Scrabble_Tile_'+data.Items[0].tileRack.charAt(i)+'.jpg'
        }
      }
    )
    .catch(reason => console.log(reason.message))

function addHandlers() {
  let tileImages = document.querySelectorAll('#rack .tile');
  [].forEach.call(tileImages, function (tile) {
    tile.addEventListener('dragstart', tileDragStart, false);
    tile.addEventListener('dragover', tileDragOver, false);
    tile.addEventListener('drop', tileDrop, false);
    tile.addEventListener('dragend', tileDragEnd, false);
  });
}

addHandlers();
