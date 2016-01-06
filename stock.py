# coding=utf-8
import csv

# Ouverture du flux
dictProduct = {}

# Cette méthode ne sert à rien mais je la laisse pour une éventualité
def sortAndCreateListProductObject():
    fileWalletTransaction = open('WalletTransactions.csv', 'rb')
    readerWalletT = csv.reader(fileWalletTransaction)
    listProductString = list()
    listProductObject = list()

    for line in readerWalletT:
        listProductString.append(line[3])
        listProductStringSet = list(set(listProductString))
        listProductStringSet.sort()

    for lineProduct in listProductStringSet:
        listProductObject.append(lineProduct)

    print listProductObject
    print listProductObject.__len__()

    fileWalletTransaction.close()


# Creation du stock initial avec tous les produits
def createInitialStock():
    fileWalletTransaction = open('WalletTransactions.csv', 'rb')
    readerWalletT = csv.reader(fileWalletTransaction)

    for line in readerWalletT:
        if testDictProduct(dictProduct, line[3]):
            continue
        else:
            dictProduct.update({line[3]: []})

    fileWalletTransaction.close()

# Ajout du stock initial à partir du csv
def addStockInitial():
    fileStockInitial = open('stock_initial.csv', 'rb')
    readerStockInitial = csv.reader(fileStockInitial)

    for line in readerStockInitial:
        lineStockInitial = line[0].split(';')

        dateStockInitial = convertDateFormat(lineStockInitial[0])

        for i in range(int(lineStockInitial[2])):
            dictProduct[lineStockInitial[1]].append(lineStockInitial[3])

    fileStockInitial.close()

def calculValeurStock():
    priceSum = 0

    for produit in dictProduct:
        for prix in dictProduct[produit]:
            priceSum = priceSum + int(prix)

    return priceSum

# maj du stock
def updateStock(date):
    fileWalletTransaction = open('WalletTransactions.csv', 'rb')
    readerWalletT = csv.reader(fileWalletTransaction)

    for line in readerWalletT:
        dateCSV = line[0].split(' ')
        if date == dateCSV[0]:
            if line[7] == 'Buy':
                for i in range(int(line[2])):
                    dictProduct[line[3]].append(line[4])
                #print 'ajout OK'
            else:
                for i in range(int(line[2])):
                    try:
                        dictProduct[line[3]].pop(0)
                        #print 'remove'
                    except:
                        continue

    fileWalletTransaction.close()

def principale():
    fileWalletTransaction = open('WalletTransactions.csv', 'rb')
    readerWalletT = csv.reader(fileWalletTransaction)
    for line in readerWalletT:
        dateCSV = line[0].split(' ')
        updateStock(dateCSV)
        c = csv.writer(open("actifStock.csv", "wb"))
        c.writerow([dateCSV,calculValeurStock()])
    fileWalletTransaction.close()

# convertis la date du stock initial au format de celui de walletTransaction
def convertDateFormat(date):
    dateFormated = date.split(';')
    dateFormated = dateFormated[0].split('/')
    dateFormated = dateFormated[2] + '-' + dateFormated[1] + '-' + dateFormated[0] + ' 00:00:00'
    return dateFormated

#test pour la création du stock initial
def testDictProduct(dictProduct, product):
    for mot in dictProduct:
        if mot == product:
            return True
        else:
            return False


#### le main ####
createInitialStock()
addStockInitial()
calculValeurStock()
principale()


print dictProduct
