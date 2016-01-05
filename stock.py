import csv;

import csv


fname = "WalletTransactions.csv"
file = open(fname, "rb")

reader = csv.reader(file)

#

for line in reader:
	p = 1
	i=0
	unitP = 0
	vararecup = line[0].split(' ', 1 )
	print line[3]

