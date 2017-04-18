import string
import json
from ast import literal_eval

def HitMissile(targetBattleShip, hittingBattleShip, curHitCord):	
	targetActiveCells = targetBattleShip.getActiveCells()	
	if curHitCord in targetActiveCells:		
		print (str(hittingBattleShip.getBattleShipId())+ ' fires a missile with target '+ str(curHitCord) +' which HIT')
		targetActiveCells[curHitCord] = targetActiveCells[curHitCord] -1
		if(targetActiveCells[curHitCord] == 0):			
			del targetActiveCells[curHitCord]			
		return 1
	else:
		print (str(hittingBattleShip.getBattleShipId())+ ' fires a missile with target' + str(curHitCord) + ' which missed')
		return 0


# this is used to pass parameters for creating tank
class Tank:
	def __init__(self, type, tankInitialCord, tankRange):
		self.type = type
		self.tankInitialCord = tankInitialCord
		self.tankRange = tankRange		

	def getType(self):
		return self.type
	def getTankInitialCord(self):
		return self.tankInitialCord
	def getTankRange(self):
		return self.tankRange

# this is main class where tank is created 
class BattleShip:
	def __init__(self,maxX,maxY,battleShipId,tanks,missileTargetsForOpponent):
		self.maxX = maxX
		self.maxY = maxY		
		self.tanks = tanks
		self.activeCells = {}
		self.battleShipId = battleShipId
		self.missileTargetsForOpponent = missileTargetsForOpponent
		self.typeDict = {'P': 1 , 'Q' : 2}

	def getBattleShipId(self):
		return self.battleShipId

	def getActiveCells(self):		
		return self.activeCells

	def getMissileTargets(self):
		return self.missileTargetsForOpponent

	# though this is not used  as of now, but can be used later if we want to draw the battle field
	def createBattleArea(self): 
		MRange = {x+1 for x in range(m)}
		NRange = {letter for letter in string.ascii_uppercase if letter <= n}

		# Create cells boundry
		cordinates = {}
		for i in NRange:
			for j in MRange:				
				cordinates[(i,j)] = 0

	# Create ship of given size and type from a given given cordinates
	def CreateShip(self):

		for tank in self.tanks:
			locationXRange = ( chr(ord(tank.tankInitialCord[0]) + n)  for n in range(tank.tankRange[0]) )			
			locationYRange = ( tank.tankInitialCord[1] + n for n in range(tank.tankRange[1]) )			
			liveCordinates = {}

			for i in locationXRange:
				for j in locationYRange:
					c = (i,j)
					self.activeCells[c] = self.typeDict[tank.type]

def main():
	# Pass json file as input
	j = open('input.json', 'r')
	data = json.load(j)	
	m = data['m']
	n = data['n']

	if(m > 9):
		print( "M should be less than 9" )
		return 

	if( n not in list(string.ascii_uppercase)):
		print( "N should be between A and Z (Capital letter Only)" )
		return 
	
	tanksBattleArea1 = []
	for tank in data['tank1']:	
		type = tank['type']	
		location = literal_eval(tank['location'])
		dimension = literal_eval(tank['dimension'])
		tanksBattleArea1.append(Tank(type,location,dimension))

	tanksBattleArea2 = []
	for tank in data['tank2']:		
		type = tank['type']	
		location = literal_eval(tank['location'])
		dimension = literal_eval(tank['dimension'])
		tanksBattleArea2.append(Tank(type,location,dimension))


	
	player1Hits = list(literal_eval(data['missileTargetsForPlayerA']))
	player2Hits = list(literal_eval(data['missileTargetsForPlayerB']))

	battleShip1 = BattleShip(10,'H',"BattleShip1",tanksBattleArea1,player1Hits)
	battleShip2 = BattleShip(10,'H',"BattleShip2",tanksBattleArea2,player2Hits)

	battleShip1.CreateShip()
	battleShip2.CreateShip()


	battleShip1hit = 0
	battleShip2hit = 0
	currentBattleShip = 1

	print "Player 1 has theese active cells " + str(battleShip1.getActiveCells())	
	print "Player 1 has these many hits: " + str(player1Hits)
	print "Player 2 has theese active cells " + str(battleShip2.getActiveCells())	
	print "Player 2 has these many hits: " + str(player2Hits)


	while(True):		
		# print "current plauer = " + str(currentBattleShip)
		if(currentBattleShip == 2 and battleShip2hit < (len(battleShip2.getMissileTargets()))):
			if(len(battleShip1.getActiveCells()) == 0):
				print (str(battleShip2.getBattleShipId()) + ' Wins the battle' )
				break		
			curentCord = battleShip2.getMissileTargets()[battleShip2hit]
			status = HitMissile(battleShip1, battleShip2 ,curentCord )
			if(status == 0):
				currentBattleShip = 1
			else:
				currentBattleShip = 2
			
			battleShip2hit = battleShip2hit + 1 
			
		elif(currentBattleShip == 1 and battleShip1hit < (len(battleShip1.getMissileTargets()))):
			if(len(battleShip2.getActiveCells()) == 0):
				print (str(battleShip1.getBattleShipId()) + ' Wins the battle' )
				break	
			curentCord = battleShip1.getMissileTargets()[battleShip1hit]
			status = HitMissile(battleShip2, battleShip1 ,curentCord)
			if(status == 1):
				currentBattleShip = 1
			else:
				currentBattleShip = 2

			battleShip1hit = battleShip1hit + 1 

		else:
			if(currentBattleShip ==1):
				print "battleShip 1 has no missiles left"
				currentBattleShip =2
			else:
				currentBattleShip = 1
				print "battleShip 2 has no missiles left"
			if (battleShip2hit+battleShip1hit >= len(battleShip1.getMissileTargets())+len(battleShip2.getMissileTargets())):
				break;

	if(len(battleShip1.getActiveCells()) == 0):
				print (str(battleShip2.getBattleShipId()) + ' Wins the battle' )
				
	if(len(battleShip2.getActiveCells()) == 0):
				print (str(battleShip1.getBattleShipId()) + ' Wins the battle' )

	if(len(battleShip1.getActiveCells()) != 0 and len(battleShip2.getActiveCells()) != 0):
		print ('Let Peace Prevail In This World' )


if __name__ == '__main__':
	main()