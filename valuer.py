from plants import *
prices = [10,20,30,40,50,60,70,80,90,100,150,200,250,300,350,400,450,500]
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
for port in portfolios:
	print port.name
	for price in prices:
		port.setBids(price)
		print price, port.calcTotalProfit(price)

