from plants import *

def sort_inner(plant):
	return plant.varCost

def get_supply(allplants, price):
	i = 0
	supply = 0
	while allplants[i].bid < price:
		supply += allplants[i].capacity
		i+=1
	return supply

def get_demand(allplants, intercept, modifier):
	demand = intercept
	price = .01
	i = 0
	supply = []
	while get_supply(allplants, price) < demand:
		price += .5
		demand = intercept + modifier * price
	return demand

def get_price(allplants, intercept, modifier):
	demand = intercept
	price = .01
	i = 0
	supply = []
	while get_supply(allplants, price) < demand:
		price += .5
		demand = intercept + modifier * price
	return price

def initialize_market(demand, allplants):
	sum = 0
	i = 0
	while sum < demand and i<len(allplants):
		p = allplants[i]
		sum += p.capacity
		clearCost = p.bid
		i+=1
	print sum, demand, clearCost
	return clearCost

def step_up(plant, allplants, clearprice):
	clearpos = 0
	l = enumerate
	for pos,p in enumerate(allplants):
		if p.bid > clearprice and clearpos <1:
			clearpos = pos
			clearbid = p.bid
			plant.bid = p.bid
			p.setBid(p.bid-.01)

	


def exercise_power(portfolio, allplants, intercept, modifier):
	pass
	""" Get profit at the current clearing price. 

	Permutation solution?
	e.g. if three plants are in the market, try A, then AB, then AC, then BC. Track which works best.
	Try moving most expensive plant up to next level.
	Track bids in an array.
	Track profits in a second array"""
	bids = []
	profits = []
	bidHistory = []
	plantsinplay = []
	clearprice = get_price(allplants, intercept, modifier)
	for p in portfolio.plants: #build a list of all plants that could be used to exercise market power
		if p.varCost < clearprice:
			plantsinplay.append(p)

	while something:
		bids = []
		while somethingElse:
			#TODO do stuff
			pass
		bidHistory.append(bids) #need to keep a list of the bids we formed.
		clearCost = get_price(allplants, intercept, modifier) #Need to know where the market clears
		p = portfolio.calcProfit(clearCost) #figure out how profitable the scenario is
		profits.append(p)

def shade_up(allplants):
	""" Shade up takes the sorted list of plants and raises every plants bid to the next level, if it is the only plant at that production level. If there is a tie with a plant from a different portfolio, the bid is shaded up $.01, to ensure that the maximum amount is captured. """
	i = 0
	while i < len(allplants):
		tieplants = []
		p = allplants[i]
		if i+1 == len(allplants):
			p.setBid(500)
		elif p.varCost < allplants[i+1].varCost: #The current plant is the only one with its MC
			p.setBid(allplants[i+1].varCost) #Bid the plant up to the step ahead MC
		else:
			tieplants.append(p) # we have a tie
			bidlow = 0 #initialize variable to check if we should bid low
			j = i + 1 #initialize variable to start checking subsequent plants
			while p.varCost == allplants[j].varCost: #It could be more than a two way, so we build a list of all plants in the tie
				tieplants.append(allplants[j])
				j += 1
			for dupe in tieplants: #check for dupes
				if dupe.owner != p.owner:
					bidlow = 1

			for dupe in tieplants: #set bids
				if bidlow:
					dupe.setBid(dupe.bid + .01)
				else:
					dupe.setBid(allplants[j].varCost)
			i = j-1 # we should pick up our bid after the last duplicate, which happens to be 'j-1'
		i += 1

portfolios = []
allplants = []
f=open('./planfile.csv', 'r')
for line in f:
	vArray = line.split(',')
	if vArray[1]:
		plant = Plant(vArray[0],vArray[1],float(vArray[2]),float(vArray[3]),float(vArray[4]),float(vArray[5]),float(vArray[6]),float(vArray[7]),float(vArray[8]))
		port.addPlant(plant)
		allplants.append(plant)
	else:
		port = Portfolio(vArray[0])
		portfolios.append(port)
allplants.sort(key=sort_inner)
intercept = input('Demand Intercept?')
modifier = input('Slope?')
shade_up(allplants)
demand = get_demand(allplants, intercept, modifier)

clearCost = initialize_market(demand, allplants)

for p in allplants:
	if p.varCost < clearCost:
		p.setBid(clearCost)

for p in allplants:
	print p.name + ' - ' + str(p.bid)

print "BIG COAL"
for p in portfolios[0].plants:
	print p.name + ' - ' + str(p.bid)
