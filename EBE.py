import csv;

fname = "WalletTransactions.csv"
file = open(fname, "rb")
from io import StringIO
csvf = StringIO(file.read().decode())
reader = csv.reader(csvf,delimiter=',')
for line in reader:
	p = 1
	i=0
	unitP = 0
	vararecup = line[0].split(' ', 1 )

file.close()