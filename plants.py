class Market:    	
    """ A model of an ESG market"""
    def __init__(self, name, plants, dIntercept, dElasticity, fixedPrice=0):
        self.name = name
        self.plants = plants
        self.dIntercept = dIntercept
        self.dElasticity = dElasticity
        self.runMarket(fixedPrice)

    def getDemand(self):
        """getDemand gradually increases price until the market clears. It stores the total quantity demanded for the market"""
    	intercept = self.dIntercept
    	demand = intercept
    	modifier = self.dElasticity
    	i = 0
    	price = self.plants[i+1].bid - .01 
    	while self.getSupply(price) < demand:
    	    i+=1
            price = self.plants[i+1].bid - .01
            demand = intercept + modifier * price
    	return demand
        	
    def getSupply(self, price):
        """getSupply calculates the available supply at a given price, and stores it"""
        i = 0
    	supply = 0
    	while self.plants[i].bid < price:
    		supply += self.plants[i].capacity
    		i+=1
    	self.supply = supply
    	return supply

    def dropPlant(self, plant):
        self.plants.remove(plant)
        self.runMarket()
        
    def addPlant(self,plant):
        i = 0
        while self.plants[i].bid < plant.bid:
            i+=1
        self.plants.insert(i,plant)
        self.runMarket()
        
    def updatePlants(self,plants):
        self.plants = plants
        self.runMarket()
        
    def runMarket(self, fixedPrice = 0):
        """runMarket returns the market clearing price. It also figures out how much excess capacity there is at this price"""
        self.qdemand = self.getDemand() #start by finding the total quantity demanded
    	sum = 0 
    	i = 0
    	if fixedPrice: #we're running an auction with a pre-set price.
    	    clearCost = fixedPrice
    	    while self.plants[i].bid < fixedPrice:
    	        p = self.plants[i]
    	        sum += p.capacity
    	        i +=1
    	else:
        	while sum < self.qdemand and i<len(self.plants): #keep going until we've met demand, or until we hit the end of the plant list
        		p = self.plants[i] #get the current plant
        		sum += p.capacity #add its capacity
        		clearCost = p.bid #update the clearing price to reflect this plant's bid
        		i+=1
    	self.residualDemand = sum - self.qdemand	
    	self.clearPrice = clearCost
    	if sum > self.qdemand:
    	    self.excessCapacity = sum - self.qdemand
    	    while i+1 < len(self.plants) and self.plants[i].bid == clearCost: #there are more plants to check for extra capacity
    	        if self.plants[i+1].bid == clearCost: #There's another plant on the market with this bid
    	            self.excessCapacity += self.plants[i+1].capacity #add it's capacity to the excess capacity figure
    	        i+=1
    	else: #There's no extra capacity in this market; price can rise fairly freely.
    	    self.excessCapacity = 0

    def findPlantByPrice(self, price):
        i = 0
        while self.plants[i].bid < price:
            i +=1
        return self.plants[i], self.plants[i+1] 

            	
class Plant:
	""" A model of an ESG plant """
	def __init__(self, name, location, capacity, heatRate, fuelPrice, fuelCost, vOM, carbon, dailyOM):
		self.name = name
		self.location = location
		self.usedCapacity = 0
		self.capacity = capacity
		self.heatRate = heatRate
		self.fuelPrice = fuelPrice
		self.fuelCost = fuelCost
		self.vOM = vOM
		self.carbon = carbon
		self.dailyOM = dailyOM
		self.setVarCost()
		self.setBid(self.varCost)

	def setBid(self,bid):
		self.bid = bid
		self.setProfit()

	def setProfit(self, cap = 0):
		self.profit = self.bid - self.varCost
		if cap:
			self.totalProfit = self.profit * cap - self.dailyOM / 4
		else:
			self.totalProfit = self.profit * self.capacity - self.dailyOM / 4

	def setVarCost(self):
		self.varCost = self.fuelCost + self.vOM

class Portfolio:
	""" A model of an ESG portfolio """
	def __init__(self, name):
		self.name = name
		self.plants = []

	def __sort_inner(self, plant):
		return plant.varCost

	def addPlant(self,plant):
		self.plants.append(plant)
		plant.owner = self.name
		self.plants.sort(key=self.__sort_inner)

	def calcProfit(self):
		profit = 0
		for plant in self.plants:
			profit += plant.profit
		return profit
	def calcTotalProfit(self):
		profit = 0
		for plant in self.plants:
			profit += plant.totalProfit
		return profit

	def setBids(self, clearingPrice):
		for plant in self.plants:
			if plant.bid < clearingPrice:
				plant.setBid(clearingPrice)


