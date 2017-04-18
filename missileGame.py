import string
import json
from ast import literal_eval

'''
This is responsible for hitting on a cell of target battle Area. This return 1 if hit was successful else returns 0
'''
def HitCell(targetBattleArea, hittingBattleArea, curHitCord):	
	targetLiveCells = targetBattleArea.getLiveCells()	
	battleAreaId = hittingBattleArea.getBattleAreaId()
	
	if curHitCord in targetLiveCells:		
		print (str(battleAreaId)+ ' fires a missile with target '+ str(curHitCord[0]) + str(curHitCord[1]) +' which hit')
		targetLiveCells[curHitCord] = targetLiveCells[curHitCord] -1
		if(targetLiveCells[curHitCord] == 0):			
			del targetLiveCells[curHitCord]			
		return 1
	else:
		print (str(battleAreaId)+ ' fires a missile with target ' + str(curHitCord[0]) + str(curHitCord[1]) + ' which missed')
		return 0

'''
BattleShip is responsible for encapsulating all input required to create a Battle Ship
'''
class BattleShip:
	'''
    defining constructor
    '''
	def __init__(self, type, positions, dimensions):
		self.type = type
		self.positions = positions
		self.dimensions = dimensions	

'''
BattleArea represents a battle field for a player. Here we create battleShips. 
Create a battle area for player.
'''

class BattleArea:
	'''
    defining constructor
    '''
	def __init__(self,maxX,maxY,battleAreaId,battleShips,missileTargets):
		self._maxX = maxX
		self._maxY = maxY		
		self.battleShips = battleShips
		self.liveCells = {}
		self.battleAreaId = battleAreaId
		self.missileTargets = missileTargets
		self.typeDict = {'P': 1 , 'Q' : 2}
		self.battleAreaCells = {}

	def getBattleAreaId(self):
		return self.battleAreaId

	def getLiveCells(self):		
		return self.liveCells

	def getMissileTargets(self):
		return self.missileTargets

	# though this is not used  as of now, but can be used later if we want to draw the battle field
	def createBattleArea(self): 
		MRange = {x+1 for x in range(self._maxX)}
		NRange = {letter for letter in string.ascii_uppercase if letter <= self._maxY}
		# Create Battle Area boundry
		for i in NRange:
			for j in MRange:				
				self.battleAreaCells[(i,j)] = 0

	# Create ship of given size and type from a given given cordinates
	def CreateShips(self):

		for battleShip in self.battleShips:
			locationXRange = ( chr(ord(battleShip.positions[0]) + n)  for n in range(battleShip.dimensions[0]) )			
			locationYRange = ( battleShip.positions[1] + n for n in range(battleShip.dimensions[1]) )			
			
			for x in locationXRange:
				for y in locationYRange:					
					self.liveCells[(x,y)] = self.typeDict[battleShip.type]


def processJSONFile(jsonFile):
	# Pass json file as input
	j = open(jsonFile, 'r')
	jsonData = json.load(j)	
	m = jsonData['m']
	n = jsonData['n']
	if(m > 9):
		print( "M should be less than 9" )
		return

	if( n not in list(string.ascii_uppercase)):
		print( "N should be between A and Z (Capital letter Only)" )
		return 

	battleShipPlayer1 = []
	for battleShip in jsonData['battleship1']:	
		type = battleShip['type']	
		location = literal_eval(battleShip['location'])
		dimension = literal_eval(battleShip['dimension'])
		battleShipPlayer1.append(BattleShip(type,location,dimension))

	battleShipPlayer2 = []
	for battleShip in jsonData['battleship2']:		
		type = battleShip['type']	
		location = literal_eval(battleShip['location'])
		dimension = literal_eval(battleShip['dimension'])
		battleShipPlayer2.append(BattleShip(type,location,dimension))

	player1TargetMissiles = list(literal_eval(jsonData['missileTargetsForPlayerA']))
	player2TargetMissiles = list(literal_eval(jsonData['missileTargetsForPlayerB']))

	return m,n,battleShipPlayer1,battleShipPlayer2,player1TargetMissiles,player2TargetMissiles

def launchMissiles(battleArea1,battleArea2):
	p1,p2 = 0,0
	currPlayer = 1
	missileTargetsP1 = battleArea2.getMissileTargets()
	missileTargetsP2 = battleArea1.getMissileTargets()	

	print ("Player 1 has these active cells " + str(battleArea1.getLiveCells()))
	print ("Player 1 has these targets to  hit: " + str(battleArea1.getMissileTargets()))
	print ("Player 2 has these active cells " + str(battleArea2.getLiveCells()))
	print ("Player 2 has these targets to  hit: " + str(battleArea2.getMissileTargets()))

	while(True):				
		if(currPlayer == 2 and p2 < len(missileTargetsP1)):			
			curentCord = missileTargetsP1[p2]
			status = HitCell(battleArea1, battleArea2 ,curentCord )
			# if there are no more active cells on opposite battle Area, then Player2 wins the battle
			if(len(battleArea1.getLiveCells()) == 0):
				print (str(battleArea2.getBattleAreaId()) + ' won the battle' )
				return	

			if(status == 0):
				currPlayer = 1
			else:
				currPlayer = 2			
			p2 = p2 + 1 
			
		elif(currPlayer == 1 and p1 < len(missileTargetsP2)):			
			curentCord = missileTargetsP2[p1]
			status = HitCell(battleArea2, battleArea1 ,curentCord)
			if(len(battleArea2.getLiveCells()) == 0):
				print (str(battleArea1.getBattleAreaId()) + ' won the battle' )
				return
			if(status == 0):
				currPlayer = 2
			else:
				currPlayer = 1
			p1 = p1 + 1 

		elif(p2+p1 >= len(missileTargetsP2)+len(missileTargetsP1)):
			if(currPlayer == 1):
				print (str(battleArea1.getBattleAreaId()) + ' has no more missiles left' )
			else:
				print (str(battleArea2.getBattleAreaId()) + ' has no more missiles left' )
			break

		# This is used for switching if any of the player has no more missiles left
		else:
			if currPlayer ==1 :
				print (str(battleArea1.getBattleAreaId()) + ' has no more missiles left' )				
				currPlayer =2
			else:
				print (str(battleArea1.getBattleAreaId()) + ' has no more missiles left' )
				currPlayer = 1	

	if(len(battleArea1.getLiveCells()) != 0 and len(battleArea2.getLiveCells()) != 0):
		print ('Players declare peace: Let Peace Prevail In This World' )

 
def main(inputFile):
	try:
		m,n,battleShipPlayer1,battleShipPlayer2,player1TargetMissiles,player2TargetMissiles = processJSONFile(inputFile)
		battleArea1 = BattleArea(m,n,"Player-1",battleShipPlayer1,player1TargetMissiles)
		battleArea2 = BattleArea(m,n,"Player-2",battleShipPlayer2,player2TargetMissiles)
		# battleArea1.createBattleArea()
		# print (battleArea1.battleAreaCells)
		battleArea1.CreateShips()
		battleArea2.CreateShips()
		launchMissiles(battleArea1,battleArea2)	
	except Exception, e:
		print ("Please pass a valid input file(json format) \n")
		raise e
	

if __name__ == '__main__':
	# main('input.json')
	# main('input_winner2.json')
	main('input_winner1.json')

# input.json file format(required as input)
# {
# 	"m":9,
# 	"n":"H",
# 	"battleship1" : [
# 		{
# 			"dimension" :  "(2,1)",
# 			"location" :  "('A',1)",
# 			"type" : "Q"
# 		},
# 		{
# 			"dimension" :  "(4,2)",
# 			"location" :  "('D',4)",
# 			"type" : "P"
# 		}
# 		],
# 	"battleship2" : [
# 		{
# 			"dimension" :  "(2,1)",
# 			"location" :  "('B',1)",
# 			"type" : "P"
# 		},
# 		{
# 			"dimension" :  "(4,2)",
# 			"location" :  "('C',3)",
# 			"type" : "P"
# 		}
# 		],
# 		"missileTargetsForPlayerA" : "('A',1) , ('B',2) , ('C',3),('B',1) , ( 'C',4 ), ( 'D',5 ),('E',1) , ( 'D',4 ), ('B',3)",
# 		"missileTargetsForPlayerB" : "('A',1) , ('B',2), ('B',3) ,   ( 'D',5)  "
# }	