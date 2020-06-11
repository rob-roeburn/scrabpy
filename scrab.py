#!/usr/bin/env python
# coding: utf-8
import random

tileBag     = {"*": 2, "A": 9, "B": 2, "C": 2, "D": 4, "E": 12, "F": 2, "G": 3, "H": 2, "I": 9, "J": 1, "K": 1, "L": 4, "M": 2, "N": 6, "O": 8, "P": 2, "Q": 1, "R": 6, "S": 4, "T": 6, "U": 4, "V": 2, "W": 2, "X": 1, "Y": 2, "Z": 1}
tileProb    = ["*"]*2+["A"]*9+["B"]*2+["C"]*2+["D"]*4+["E"]*12+["F"]*2+["G"]*3+["H"]*2+["I"]*9+["J"]*1+["K"]*1+["L"]*4+["M"]*2+["N"]*6+["O"]*8+["P"]*2+["Q"]*1+["R"]*6+["S"]*4+["T"]*6+["U"]*4+["V"]*2+["W"]*2+["X"]*1+["Y"]*2+["Z"]*1
numPlayers  = 4
rackSize    = 7
round       = 1
reshuffle   = '***RESHUFFLE'

def getValidTile(tileRack, tileInt):
    letter=random.choice(tileProb)
    if (tileBag[letter] < 1):  # tile bag does not contain any more of the desired letter, so recurse with a new rand
        tileRack = getValidTile(tileRack, tileInt)
        return tileRack
    tileBag[letter] = tileBag[letter]-1 # tile bag contained desired letter, so subtract that dict element from the bag
    tileRack[tileInt] = letter # set desired letter to tileInt element in rack
    return tileRack

def buildNewRack(): # return a dict of available tiles from the tile bag
    tileRack = {}
    for i in range(0, rackSize):
        tileRack = getValidTile(tileRack, i)
    return tileRack

def buildRacks(numPlayers): # return a dict list of randomly generated racks matching the number of players
    playerRacks = {}
    for i in range(0, numPlayers):
        playerRacks[i] = buildNewRack()
        print(list(playerRacks[i].values()))
    return playerRacks

def updateRack(playerRack, letter): # take letter arg and update with another random from the bag, or return shrunk playerRack if not
    if (sum(tileBag.values()) < 1): # tile bag is empty, pop the letter and send the rack back shrunk by one
        playerRack.pop(list(playerRack.keys())[list(playerRack.values()).index(letter.upper())])
        return playerRack
    else: # replace the letter being used with another valid one from the tile bag
        playerRack = getValidTile(playerRack, list(playerRack.keys())[list(playerRack.values()).index(letter.upper())])
    return playerRack

def reshuffleRack(playerRack): # send all tiles in player rack back to the tile bag and return a new random rack
    for tile in (playerRack):
        tileBag[playerRack[tile]] = tileBag[playerRack[tile]]+1
    return buildNewRack()

def validateLetters(letters): # ensure all letters to play exist in rack. if any do not, recurse validate and prompt again until they do
    for index,element in enumerate(letters):
        if (not element.upper() in playerRacks[i-1].values()):
            print (element+" does not exist in the player rack. Please try again.")
            letters = input("Which letters to use? ")
            if letters != reshuffle:
                letters = validateLetters(letters)
            return letters
    return letters

def countPlayerTiles(playerRacks): # helper function to monitor remaining player tiles. when all remaining player tiles are 0, main loop will exit
    playerTiles = 0
    for playerRack in playerRacks:
        playerTiles += len(playerRacks[playerRack].values())
    return playerTiles


def updateDynamo(gameId, playerId, playerRacks):
    payload = {'gameId': str(gameId), 'playerId': str(i), 'tileRack': ''.join(str(e) for e in playerRacks[i-1].values())}
    r = requests.post('https://8n831lmsk9.execute-api.eu-west-1.amazonaws.com/main/scrabUpdate/a/b', data=json.dumps(payload))

playerRacks = buildRacks(numPlayers)
playerTiles = countPlayerTiles(playerRacks)

# main loop
while playerTiles > 0:
    for i in range(1, numPlayers+1):
        playerTiles = countPlayerTiles(playerRacks)
        print("Round "+str(round)+", Player "+str(i)+"\'s turn. "+str(sum(tileBag.values()))+" tiles remaining in bag, "+str(playerTiles)+" total player tiles remaining.\n")
        print(*tileBag.values(), sep = " ")
        print(*playerRacks[i-1].values(), sep = " ")
        updateDynamo(333, i, playerRacks)
        letters = input("Which letters to use? ")
        if letters == reshuffle:
            playerRacks[i-1] = reshuffleRack(playerRacks[i-1])
        else:
            if letters != reshuffle:
                letters = validateLetters(letters)
                if letters != reshuffle:
                    for index,element in enumerate(letters):
                        playerRacks[i-1] = updateRack(playerRacks[i-1], element)
                else:
                    playerRacks[i-1] = reshuffleRack(playerRacks[i-1])
        updateDynamo(333, i, playerRacks)
    round += 1
