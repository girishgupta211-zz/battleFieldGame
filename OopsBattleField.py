import string
import pprint as pprint

def validateShipRange(func):
	def inner_func(self,location, dimention, type,maxX,maxY ):
		# print location
		# # print dimention
		# # print type
		# print maxX
		# print maxY
		x =ord(location[0]) - 64
		y = location[1]
		# print x
		# print y
		# print x+dimention[0]-1
		# print y+dimention[1]-1

		if (x+dimention[0]-1 > maxX and y+dimention[1]-1 < ord(maxY) - 64):
			raise Exception("tanks should be within battle field")

	
		return func(self,location,dimention,type,maxX,maxY)
	return inner_func


def validateRange(func):
	def inner_func(self,X, Y, id):
		print X
		print Y
		if X > 9:
			raise Exception("M needs to be less than 9")		
		if( Y not in list(string.ascii_uppercase)):
			raise Exception( "N should be between 'A' and 'Z' (Capital letter Only)" )		
		
		return func(self,X,Y,id)
	return inner_func


# def validateTank(func):
# 	def inner_func(self,X, Y, id):
# 		if X > 9:
# 			raise Exception("M needs to be less than 9")		
# 		if( Y not in list(string.ascii_uppercase)):
# 			raise Exception( "N should be between 'A' and 'Z' (Capital letter Only)" )		
		
# 		return func(self,X,Y,id)
# 	return inner_func


class BattleArea(object):
	@validateRange
	def __init__(self,maxX,maxY,battleShipId):		
		self.maxX = maxX
		self.maxY = ord(maxY) - 64
		self.battleShipId = battleShipId		
		# self.createBattleArea()		

	def getBattleAreaId(self):
		return self.battleShipId

	def createBattleArea(self):
		self.battleArea = [[0 for i in xrange(self.maxX)] for i in xrange(self.maxY)] 
		# pprint.pprint (battleArea)

# this is used to pass parameters for creating tank
class Ship(BattleArea):
	@validateShipRange
	def __init__(self, location, dimention,type,maxX,maxY):				
		self.location = location
		self.dimention = dimention
		self.type = type		
		BattleArea.__init__(self,maxX, maxY, 'A')


class BattleField(BattleArea):
	totalPower = 0
	def __init__(self, m,n,battleFieldId,tanksArry):
		BattleArea.__init__(self,m,n,battleFieldId)
		self.createBattleArea()		
		self.populateBattleField(tanksArry)
	
	def populateBattleField(self,tanksArry):
		for tank in tanksArry:
			print tank.location
			print tank.dimention
			print tank.type

			x =ord(tank.location[0]) - 64
			y = tank.location[1]
			xRange = [ x + i  for i in range(tank.dimention[0]) ]
			yRange = [ y + i  for i in range(tank.dimention[1]) ]
			
			power = {}
			power['P'] = 1
			power['Q'] = 2
			print xRange
			for i in xRange:
				for j in yRange:
					self.battleArea[i-1][j-1] = power[tank.type]
					self.totalPower += power[tank.type]
		pprint.pprint (self.battleArea)


def play():
	m = 9
	n = 'G'

	battleArea1 = BattleArea(m,n,"BattleArea1")	
	# battleArea1.createBattleArea()

	location = ('A',3)
	dimention = (3,4)
	type = 'P'

	tanksBattleArea1 = []
	tanksBattleArea1.append(Ship(location,dimention,type,m,n))
	tanksBattleArea1.append(Ship( ('F', 8) ,(2,2),'Q',m,n))
	# pprint.pprint (tanksBattleArea1[0].location)
	battleField1 = BattleField(m,n,"BattleArea1",tanksBattleArea1)
	print battleField1.totalPower
	# targetsPlayerRaw1 = [('A',1) , ('B',2) , ('B',2), ('B',3)]
	# process(target)
	targetsPlayer1 = [(1,1) , (2,2) , (2,2), (2,3)]


	# missileTargetsForPlayerA
	


	# tank = Ship(location,dimention,type,m,n)


if __name__ == '__main__':
	play()
