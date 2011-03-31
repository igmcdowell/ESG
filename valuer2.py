from plants import *
prices = [27.5, 29.5, 33, 42.5, 52.5]
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
columns = []
i = 0
for port in portfolios:
	columns.append([])
	columns[i].append(port.name)
	for price in prices:
		port.setBids(price)
		columns[i].append(port.calcTotalProfit(price))
	i += 1

print columns
i = 0
j = 0
while i < len(columns[0]):
	row = ''
	while j < len(columns):
		row += ',' + str(columns[j][i])
		j +=1
	print row
	j = 0
	i += 1

