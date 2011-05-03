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


portfolios = []
northplants = []
southplants = []
allplants = []
f=open('./planfile.csv', 'r')
for line in f:
    vArray = line.split(',')
    if vArray[1]:
        plant = Plant(vArray[0],vArray[1],float(vArray[2]),float(vArray[3]),float(vArray[4]),float(vArray[5]),float(vArray[6]),float(vArray[7]),float(vArray[8]))
        port.addPlant(plant)
        allplants.append(plant)
        if(plant.location == '"North"'):
		    northplants.append(plant)
        else:
            southplants.append(plant)
    else:
		port = Portfolio(vArray[0])
		portfolios.append(port)

northplants.sort(key=sort_inner)
southplants.sort(key=sort_inner)
allplants.sort(key=sort_inner)

#shade_up(northplants)
#shade_up(southplants)
def simAuction(dn, ds, debug):
    linecap = 750
    movetotal = 0
    northmarket = Market("North Market", northplants, dn[0], dn[1])
    southmarket = Market("South Market", southplants, ds[0], ds[1])
    fullmarket = Market("Full Market", allplants, dn[0]+ds[0], dn[1]+ds[1])
    clearf = fullmarket.clearPrice
    clearn = northmarket.clearPrice
    clears = southmarket.clearPrice

    if clearn > clears: #we need to move plants from the south (low) to north (high)
        highmarket = northmarket
        lowmarket = southmarket
        dir = "ns"
    
    else: #we need to move plants from the north (low) to south (high)
        highmarket = southmarket
        lowmarket = northmarket
        dir = "sn"
    
    
    clearh = highmarket.clearPrice
    clearl = lowmarket.clearPrice
    if debug:
        print "Without moving power, high market = %s on %s and low market = %s on %s" % (clearh, highmarket.qdemand, clearl, lowmarket.qdemand)
    movedplants = []
    notdone = 1

    while notdone and movetotal < linecap:
        lowmarket.runMarket()
        clearl = lowmarket.clearPrice
        nextlowp = lowmarket.findPlantByPrice(clearl)[1]
        if nextlowp.bid < highmarket.clearPrice: #There's something to be gained by shifting a whole plant's worth of demand
            if lowmarket.excessCapacity < linecap - movetotal: #there's enough extra capacity to shift the full excess capacity
                # shift demand from the high market and update the move total
                lowmarket.dIntercept += lowmarket.excessCapacity 
                highmarket.dIntercept -= lowmarket.excessCapacity  
                movetotal += lowmarket.excessCapacity
                #re-run the high market to get the new clear price
                highmarket.runMarket() 
                clearh = highmarket.clearPrice
                if clearh > nextlowp.bid: #if the high market is still higher than the next low plant, we want to nudge things and try again
                    highmarket.dIntercept -= 1
                    lowmarket.dIntercept +=1
                    movetotal += 1
                else: #we're done, the high market price has dropped sufficiently
                    notdone = 0 
            else: #there's not enough to shift all of it, but we can still shift some
                maxMove = linecap - movetotal
                lowmarket.dIntercept += maxMove
                highmarket.dIntercept -= maxMove
                movetotal = linecap
        else: #there's not a cheap plant to move, we're done with the loop
            notdone = 0
     
    lowmarket.runMarket()
    highmarket.runMarket()
    if debug:
        print "Low market price: %s, High market price %s" %(lowmarket.clearPrice, highmarket.clearPrice)
        print "Bid of next plant in low market not running: %s, leftover capacity at current plant: %s" % (nextlowp.bid, lowmarket.excessCapacity)
    if movetotal == linecap: #We maxed out capacities, the markets are different:
        pass
    else: #the markets are merged
        spareL = linecap - movetotal
        spareC = lowmarket.excessCapacity
        spareD = highmarket.residualDemand
        if spareD < spareL:#there's enough room on the line to satisfy the excess demand
            if spareD > spareC: #there's too much demand for the supply of the last producing plant, we're settling on the high market
                lowmarket.clearPrice = highmarket.clearPrice
    if debug:
        print "Total adjusted demanded is %s in %s, %s in %s, and %s for the merged market" % (highmarket.qdemand, highmarket.name, lowmarket.qdemand, lowmarket.name, fullmarket.qdemand)
        print "final clear price low: %s, final clear price high: %s, full market: %s" % (clearl, clearh, clearf)
    return highmarket, lowmarket,movetotal,dir


demands = []
df=open('./demands.csv', 'r')
for line in df:
    dArray = line.split(',')
    dn = [float(dArray[0]), float(dArray[1])]
    ds = [float(dArray[2]), float(dArray[3])]
    demands.append((dn,ds))

p = portfolios[0]
coaltotal = 0
for dn,ds in demands:
    p.resetBids()
    highmarket, lowmarket,movetotal, dir = simAuction(dn, ds, 0)
    if lowmarket.name == "North Market":
        northmarket = lowmarket
        southmarket = highmarket
    else:
        northmarket = highmarket
        southmarket = lowmarket
    p.setBids(southmarket.clearPrice)
    
    print southmarket.clearPrice,northmarket.clearPrice, movetotal, dir, p.calcTotalProfit()
    coaltotal+= p.calcTotalProfit()
    #northmarket.updatePlants(shade_up(northmarket.plants))
    #southmarket.updatePlants(shade_up(southmarket.plants))
print coaltotal
print p.name


for port in portfolios:
    if port.plants[0].location == '"North"':
        port.setBids(northmarket.clearPrice)
    else:
        port.setBids(southmarket.clearPrice)
