from plants import *

def sort_inner(plant):
	return plant.varCost

def shade_up(allplants):
	""" Shade up takes the sorted list of plants and raises every plants bid to the next level, if it is the only plant at that production level. If there is a tie with a plant from a different portfolio, the bid is shaded up $.01, to ensure that the maximum amount is captured. """
	i = 0
	while i < len(allplants):
		tieplants = []
		p = allplants[i]
		if i+1 == len(allplants):
			p.setBid(500)
		elif p.varCost < allplants[i+1].varCost: #The current plant is the only one with its MC
			p.setBid(allplants[i+1].varCost - .01) #Bid the plant up to the step ahead MC
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
					dupe.setBid(allplants[j].varCost - .01)
			i = j-1 # we should pick up our bid after the last duplicate, which happens to be 'j-1'
		i += 1
	return allplants

carbonPrice = 0
while carbonPrice < 220:
    portfolios = []
    allplants = []
    f=open('./plantfile2.csv', 'r')
    for line in f:
        vArray = line.split(',')
        if vArray[1]:
            plant = Plant(vArray[0],vArray[1],float(vArray[2]),float(vArray[3]),float(vArray[4]),float(vArray[5]),float(vArray[6]),float(vArray[7]),float(vArray[8]), carbonPrice)
            port.addPlant(plant)
            allplants.append(plant)
        else:
    		port = Portfolio(vArray[0])
    		portfolios.append(port)
    allplants.sort(key=sort_inner)



    demands = []
    df=open('./demands.csv', 'r')
    print "Carbon at $" + str(carbonPrice)
    thiscarbon = 0
    for line in df:
        dArray = line.split(',')
        intercept = dArray[0]
        slope = dArray[1]
        themarket = Market("Combined", allplants, float(intercept), float(slope))
        themarket.runMarket();
        print themarket.carbonProduced
        thiscarbon += themarket.carbonProduced
    print "carbon "
    print thiscarbon

    carbonPrice += 20


