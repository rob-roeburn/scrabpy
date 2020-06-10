# scrab.py

![alt text](https://github.com/rob-roeburn/scrabpy/blob/master/scrablogo.png "Scrabble!")

This script can be run to simulate the available tiles in the standard version of Scrabble.  Defaulting to 4 players and 7 tiles per tile rack. The script will run and prompt for letters to be used on the board, and refresh the tile rack with available tiles from the bag.

The script supports skipping turns, reshuffling entire rack, and accurately simulates the probability of drawing tiles (12 times more likely to draw an E as a Q at the start of the game!)

The script writes each player rack to a DynamoDB table by talking to a deployed API and using the scrabUpdate lambda. The player racks can be retrieved using a combination of a deployed Amplify page from the Public directory, which talks the same API firing the scrabState lambda.

## Coming soon!

Obfuscate player and game identification - at the emoment it's easy to snoop on another player's tiles by switching out 1,2,3,4 in the query string. This should be replaced with a randomly generated string to identify game and player.

The script only writes a single game - need to implement check for pre-existing game and update, or create new.

It would also be nice to have the board simulated accurately with scoring, valid words applied - this is a much (much!) larger project.

