import numpy as np
import matlab.engine
import csv

""" NFL Field Variables """
numTeams = 32
winnerIndex = 4
loserIndex = 6
gamesPlayed = 16
teamList = []
teamFile = "NFL Teams.txt"
dataFile = "NFL Game Data.csv"

#returns index of maximum value in given list
def maxIndex(numList):
	maxIndex = 0
	maximum = 0
	counter = 0
	for num in numList:
		if num > maximum:
			maximum = num
			maxIndex = counter
		counter+=1
	return maxIndex

#contructs list of team names given relevant file
def getTeamInfo(fileName):
	teams = open(fileName, "r")
	teams_reader = csv.reader(teams)
	
	for line in teams_reader:
		teamList.append(line[0])
	
	return teamList

#returns index value of given team
def getTeamNum(teamName):
	counter = 0
	
	for team in teamList:
		if (team == teamName):
			return counter
		counter+=1
	return counter
			
#constructs the row of A matrix pertaining to a given team
def constrTeamArray(teamNum, fileName):
	games = open(fileName, "r")
	game_reader = csv.reader(games)
	gameList = [0]*numTeams
	teamName = teamList[teamNum]
	
	indices = [0]*numTeams
	
	for line in game_reader:
		if line[winnerIndex] == teamName:
			oppNum = getTeamNum(line[loserIndex])
			if indices[oppNum] == 0:
				gameList[oppNum] = 1/gamesPlayed
			else:
				gameList[oppNum] = (gameList[oppNum] + 1/gamesPlayed)/2
			indices[oppNum]+=1
		elif line[loserIndex] == teamName:
			oppNum = getTeamNum(line[winnerIndex])
			if indices[oppNum] > 0:
				gameList[oppNum] = gameList[oppNum]/2
			indices[oppNum]+=1
			
	return gameList

#prints matrix values for given team and calculates win total	
def printTeamWins(teamNum, fileName):
	gameList = constrTeamArray(teamNum, fileName)
	
	print(teamList[teamNum])
	
	counter = 0
	for game in gameList:
		if(game > 0):
			print(teamList[counter], game)
		counter+=1

#constructs the A matrix given game data file
def constrMatrix(fileName):
	counter = 0
	matrix = []
	
	for team in teamList:
		matrix.append(constrTeamArray(counter, fileName))
		counter += 1
	
	return matrix	

###### Actual Script ######

#make matrix representing game outcomes
teamList = getTeamInfo(teamFile)

A = np.array(constrMatrix(dataFile)).T.tolist()

B = matlab.double(A)

#allows me to use matlab functions within python
eng = matlab.engine.start_matlab()

#grab decomposition of said matrix
[V,D] = eng.eig(B, nargout=2)

#find dominant eigenvalue
eigVals = []
for vector in D:
	eigVals.append(eng.norm(vector))
	
V = np.array(V).T
	
convVector = V[maxIndex(eigVals)]

#sort based on values in corresponding eigenvector
Z = [x for y, x in sorted(zip(convVector, teamList))]
print(Z)

eng.quit()
