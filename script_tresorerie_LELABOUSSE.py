#!/usr/bin/python
# vim: set fileencoding=utf-8 :
 
#
# Fichier: col-1-and-3.py
#
 
import csv

fname = "WalletTransactions.csv"
file = open(fname, "rb")

total = 0.0
data = dict()

reader = csv.reader(file)
for line in reader:
	p = 1
	i=0
	unitP = 0
	vararecup = line[0].split(' ', 1 )

	if 'E' in line[4]:
		x = line[4].split('E',1)
		j = int(x[1])
		while i < j :
			p = p*10
			i = i+1
		unitP = float(x[0])*p
	else :
		unitP = float(line[4])*p

	if line[7] == "Buy":
		total = -1*float(line[2])*unitP
	else:
		total = float(line[2])*unitP
	
	if data.has_key(vararecup[0]):
		data[vararecup[0]] += total
		
	else :
		data[vararecup[0]] = total
#Création du ficher csv	
c = csv.writer(open("tresorerie.csv", "wb"))
for key, value in data.iteritems() :
	c.writerow([key,value])

file.close()