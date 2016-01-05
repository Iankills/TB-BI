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

#Création du ficher csv
c = csv.writer(open("stock.csv", "wb"))
for key, value in data.iteritems() :
	c.writerow([key,value])

file.close()