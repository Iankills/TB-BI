#!python3
#
#	Alexandre Levavasseur - FIP16
# Pour le groupe projet CO32B1
# 
#	This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License
#
# Sources:
# https://docs.python.org/3/library/csv.html
# https://docs.python.org/3/tutorial/datastructures.html
# https://docs.python.org/3/library/functions.html#int
# https://docs.python.org/3.0/library/datetime.html
# https://docs.python.org/3.0/library/time.html#time.strptime
# http://stackoverflow.com/questions/3688602/sum-numbers-in-an-array
# https://docs.python.org/3/library/decimal.html
# http://stackoverflow.com/questions/4053924/python-parse-date-format-ignore-parts-of-string
# https://docs.python.org/3/tutorial/errors.html
# http://stackoverflow.com/questions/3294889/iterating-over-dictionaries-using-for-loops-in-python
# 
import csv
from decimal import *
from datetime import datetime
import sys
from pprint import pprint

init_file = "stock_initial.csv"
in_file = "WalletTransactions.csv" # Doit être ordonné par date croissante
products = {} # dict [{'nb': x, 'price': x}, ..] ## Le stock

# #############################################################################

# Initialise le stock ..
#
def constr_init_stock_price():
	with open(init_file, newline='') as csvfile:
		reader = csv.DictReader(csvfile, delimiter=';')
		for row in reader:
			data = {'date': datetime.strptime(row['date'], '%d/%m/%Y'),
							'nb': int(row['quantity']),
							'price': Decimal(row['price'])}
			products[row['type']] = [data]

# Construit une liste des (date, qté, prix) par produit
def constr_stock_price():
	with open(in_file, newline='') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			if (row['transactionType'] == "Buy"):
				data = {'date': datetime.strptime(row['date'], '%Y-%m-%d %H:%M:%S'),
#				data = {'date': datetime.strptime(row['date'].split(' ')[0], '%Y-%m-%d'),
								'nb': int(row['quantity']),
								'price': Decimal(row['price'])}
				if (not row['type'] in products): # Produit inconnu
					products[row['type']] = [data]
# Pas date compliant
#				elif (products[row['type']][-1]['price'] == row['price']): # Si le dernier a le même prix
#					products[row['type']][-1]['nb'] = products[row['type']][-1]['nb'] + data['quantity']
				else: # Ajoute un nouveau prix
					products[row['type']].append(data)
	
	return products

# Consomme un produit en stock et retourne la liste des prix d'achat
#
def consume(product, nb, cons_date):
	out = [] # Retourne la liste des prix
	if (nb > 0):
		if (not product in products):
			raise Exception('Pas de prix pour ce produit ("%s") ?' % product)
		else:
			while (nb > 0):
				if (not products[product]): # On a vidé les stock ..
					raise Exception('Plus de prix pour ce produit ("%s")'% product)
				elif (products[product][0]['date'] > cons_date):
					raise Exception('Il reste du stock pour ("%s") mais il est ajouté après la vente..'% product)
				elif (nb >= products[product][0]['nb']): # On consomme totalement ce prix
					nb = nb - products[product][0]['nb']
					out.append(products[product].pop(0))
				else: # Sinon on prend ce qui nous intéresse et on retire du stock
					products[product][0]['nb'] = products[product][0]['nb'] - nb
					out.append({'nb': nb, 'price': products[product][0]['price']})
					nb = 0
			# end while
			return out
		# end if 2
	# end if 1
	else:
		raise Exception('On retire 0 ?')

# Calcule le montant à partir d'une liste de qté & prix
#
def calc_amount(prices): 
	amount = Decimal(0)
	for line in prices:
		amount = amount + line['price']*line['nb']
	return amount

# Calcule la marge d'une vente en fonction DES prix d'achats en question
#
def calc_marge(px_vente, pxs_achat):
	price = Decimal()
	nb = sum(px['nb'] for px in pxs_achat) # Nombre de produits vendus
	price = px_vente - calc_amount(pxs_achat)/nb # Prix de vente - moyenne prix d'achat
	return price

# Calcule la liste des marge par produit et par transaction
# à partir de la liste des entrées en stock et des ventes
#
def marge_par_trans():
	out = {} # dict de {'transId': , 'date': , 'marge': }
	with open(in_file, newline='') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			if (row['transactionType'] == "Sell"):
				if (not row['type'] in out):
					out[row['type']] = []
				this_date = datetime.strptime(row['date'], '%Y-%m-%d %H:%M:%S')
				try:
					marge = calc_marge(Decimal(row['price']), consume(row['type'], int(row['quantity']), this_date))
					out[row['type']].append({'transId': row['transID'],
															'date': this_date,
															'nb' : int(row['quantity']),
															'marge': marge})
				except Exception as e:
					print("/!\ Exception : "+e.args[0])
					print("Produit : %s\nDate conso: %s\nProduits restants: " % (row['type'], this_date))
					pprint(products[row['type']])
					print()
					break
	
	return out

# Calcule (moy pondérée) la liste des marge par produit et par jour
# en partant de la liste des marge par produit et par transaction
def marge_par_day(marges_trans):
	marge_day = {}
	for produit,translist in marges_trans.items(): # Pour chaque produit
		marge_day[produit] = {}
		for trans in translist: # Pour chaque date
			marge_day[produit][trans['date'].date()] = [];
			for search in translist: # On cherche les autres dates identiques
				if (search['date'].date() == trans['date'].date()):
					marge_day[produit][trans['date'].date()].append(search)
			nb_day = sum(i['nb'] for i in marge_day[produit][trans['date'].date()]) # nombre de ventes ce jour
			day = sum(i['nb']*i['marge'] for i in marge_day[produit][trans['date'].date()])/nb_day # moy pond.
			marge_day[produit][trans['date'].date()] = round(day, 2)
	return marge_day

# #############################################################################
# Execution
# #############################################################################

# Construit la liste des prix en stock
constr_init_stock_price()
constr_stock_price()

# DEBUG & Test
DEBUG = False
#DEBUG = True
if (DEBUG):
	pprint(products)
	print('--Consommé')
	nb = 19
	prices = consume('Small Armor Repairer II', nb, datetime.strptime('2010-09-07 00:00:00', '%Y-%m-%d %H:%M:%S'))
	pprint(prices)
	print('--Restant')
	pprint(products['Small Armor Repairer II'])
	print('--Amount consommé')
	pprint(calc_amount(prices))
	print('--Marge calculée')
	pprint(calc_marge(Decimal('271999.99'), prices))
	print()

# Main
marges_trans = marge_par_trans()
if (DEBUG):
	pprint(marges_trans)
fin = marge_par_day(marges_trans)
if (DEBUG):
	pprint(fin)
if (DEBUG):
	pprint(len(products))
	pprint(len(marges_trans)) # 1 produit n'est pas vendu
	pprint(len(fin))

print("produit,date,marge")
for produit,marges in fin.items():
	for date, marge in marges.items():
		print("%s,%s,%s" % (produit, date.strftime('%Y-%m-%d'), str(marge)))

sys.exit(0)

## POUR PIERRE ##
# you owe me :p
#
def calc_val_stock(calc_date):
	val = Decimal(0)
	for name,product in products.items():
		for stock in product:
			if (stock['date'] <= calc_date):
				val = val + stock['nb']*stock['price']
	return val
#
#
current_date = datetime.strptime('2010-07-17 00:00:00', '%Y-%m-%d %H:%M:%S')
with open(in_file, newline='') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		if (row['transactionType'] == "Sell"):
			this_date = datetime.strptime(row['date'].split(' ')[0], '%Y-%m-%d')
			if (current_date != this_date):
				print(current_date.strftime('%Y-%m-%d')+" : "+str(calc_val_stock(current_date)))
				current_date = this_date
			consume(row['type'], int(row['quantity']), this_date)
##