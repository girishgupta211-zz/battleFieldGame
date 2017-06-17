import string
from pprint import pprint 

def validateShipRange(func):
	def inner_func(self,location, dimention, type,maxX,maxY ):		
		x =ord(location[0]) - 64
		y = location[1]		

		if ( x+dimention[0]-1 > maxX or  y+dimention[1]-1 > ord(maxY) - 64):
			raise Exception("tanks should be within battle field dimention of " + str(maxX) + " by " + str(maxY))

		# if (type )

	
		return func(self,location,dimention,type,maxX,maxY)
	return inner_func


def validateRange(func):
	def inner_func(self,X, Y):
		if X > 9:
			raise Exception("M needs to be less than 9")		
		if( Y not in list(string.ascii_uppercase)):
			raise Exception( "N should be between 'A' and 'Z' (Capital letter Only)" )		
		
		return func(self,X,Y)
	return inner_func


class BattleArea(object):
	@validateRange
	def __init__(self,maxX,maxY):		
		self.maxX = maxX
		self.maxY = ord(maxY) - 64

	def createBattleArea(self):
		self.battleArea = [ [0 for i in xrange(self.maxX)] for i in xrange(self.maxY) ]


class Ship(BattleArea):
	@validateShipRange
	def __init__(self, location, dimention,type,maxX,maxY):				
		self.location = location
		self.dimention = dimention
		self.type = type
		BattleArea.__init__(self,maxX, maxY)


class BattleField(BattleArea):
	totalPower = 0
	def __init__(self, m,n,tanksArry):
		BattleArea.__init__(self,m,n)
		self.createBattleArea()		
		self.populateBattleField(tanksArry)
	
	def populateBattleField(self,tanksArry):		
		for tank in tanksArry:
			x = tank.location[1]
			y =ord(tank.location[0]) - 64			
			xRange = [ x + i  for i in range(tank.dimention[0]) ]
			yRange = [ y + i  for i in range(tank.dimention[1]) ]			
			power = { 'P':1 , 'Q':2 }			
			for i in xRange:
				for j in yRange:
					self.battleArea[i-1][j-1] = power[tank.type]
					self.totalPower += power[tank.type]
		# pprint.pprint (self.battleArea)


def run():
	m = 9
	n = 'H'
	location = ('A',1)
	dimention = (1,2)
	type = 'P'
	
	tanksBattleArea1 = []
	tanksBattleArea1.append(Ship(location,dimention,type,m,n))
	# tanksBattleArea1.append(Ship( ('H', 7) ,(2,2),'Q',m,n))	
	battleField1 = BattleField(m,n,tanksBattleArea1)

	tanksBattleArea2 = []
	tanksBattleArea2.append(Ship(location,dimention,type,m,n))
	# tanksBattleArea2.append(Ship( ('D', 3) ,(2,2),'Q',m,n))	
	battleField2 = BattleField(m,n,tanksBattleArea2)

	targetsPlayer1 = [(1,1) , (1,3),  (1,2) ]
	targetsPlayer2 = [(1,1) , (2,2) , (2,2), (2,3)]
	play(battleField1,battleField2,targetsPlayer1,targetsPlayer2)	

def hitMissile(battleField1,target):
	# pprint (battleField1.battleArea)	
	# pprint (battleField1.totalPower)
	# pprint (battleField1.battleArea[target[0]][target[1]])
	# check if target shell is an active shell( having power (1 or 2))
	# pprint (battleField1.totalPower)	
	if(battleField1.battleArea[target[0]-1][target[1]-1] > 0):
		battleField1.battleArea[target[0]-1][target[1]-1] -= 1
		battleField1.totalPower -= 1
		return True
	else:
		return False


	# pprint (battleField1.battleArea)
	# pprint (battleField1.totalPower)

	# print target

	pass

def play(battleField1,battleField2,targetsPlayer1,targetsPlayer2):	
	currPlayer = 1 
	status = False
	while(True):
		if(battleField1.totalPower == 0):
			print ("Player-2 won the battle")
			break
		if(battleField2.totalPower == 0):
			print ("Player-1 won the battle")
			break

		if(len(targetsPlayer1) == 0 and len(targetsPlayer2) == 0):
			print ("Player-1 and Player-2 have no more missiles left. players declare peace.")
			break

		if(len(targetsPlayer1) == 0):
			print ("Player-1 no more missiles left")
			currPlayer = 2			

		if(len(targetsPlayer2) == 0):
			print ("Player-2 no more missiles left")
			currPlayer = 1			

		# print targetsPlayer1
		if(currPlayer == 1):
			target = targetsPlayer1.pop(0)			
			status = hitMissile(battleField2, target)
			if(status):
				print ("Player-1 fires a missile with target " +  str(target) + " which hit")
				currPlayer = 1				
			else:
				print ("Player-1 fires a missile with target " +  str(target) + " which missed")
				currPlayer = 2
			
		else:	
			target = targetsPlayer2.pop(0)			
			status = hitMissile(battleField1, target)
			if(status):
				print ("Player-2 fires a missile with target " +  str(target) + " which hit")
				currPlayer = 2			
			else:
				print ("Player-2 fires a missile with target " +  str(target) + " which missed")
				currPlayer = 1
	
if __name__ == '__main__':
	run()
