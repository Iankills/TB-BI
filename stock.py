# coding=utf-8
import csv

# Ouverture du flux
dictProduct = {}
valeurStock = 0

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
    global valeurStock

    for line in readerStockInitial:
        lineStockInitial = line[0].split(';')

        dateStockInitial = convertDateFormat(lineStockInitial[0])

        for i in range(int(lineStockInitial[2])):
            dictProduct[lineStockInitial[1]].append(lineStockInitial[3])
        valeurStock = int(lineStockInitial[2])*int(lineStockInitial[3])

    fileStockInitial.close()

def calculValeurStock():
    priceSum = 0

    for produit in dictProduct:
        for prix in dictProduct[produit]:
            price = testExpo(prix)
            priceSum = priceSum + float(price)

    return priceSum

def testExpo(line):
    p = 1
    i=0

    if 'E' in line:
        x = line.split('E',1)
        j = int(x[1])
        while i < j :
            p = p*10
            i = i+1
        unitP = float(x[0])*p
    else :
        unitP = float(line)*p

    return unitP

# maj du stock
def updateStock(date):
    fileWalletTransaction = open('WalletTransactions.csv', 'rb')
    readerWalletT = csv.reader(fileWalletTransaction)

    for line in readerWalletT:
        dateCSV = line[0].split(' ')
        if date == dateCSV[0]:
            if line[7] == 'Buy':
                for i in range(int(line[2])):
                    prix = testExpo(line[4])
                    dictProduct[line[3]].append(prix)
                    valeurStock = valeurStock + prix
                #print 'ajout OK'
            else:
                for i in range(int(line[2])):
                    prix = testExpo(line[4])
                    try:
                        dictProduct[line[3]].pop(0)
                        valeurStock = valeurStock - prix
                        #print 'remove'
                    except:
                        continue

    fileWalletTransaction.close()

def principale(c):
    fileWalletTransaction = open('WalletTransactions.csv', 'rb')
    readerWalletT = csv.reader(fileWalletTransaction)

    dateOld = '0'
    for line in readerWalletT:
        dateCSV = line[0].split(' ')
        updateStock(dateCSV[0])
        if (dateOld!=dateCSV[0]):
            #price = calculValeurStock()
            lineAdd = str(dateCSV[0]) + ',' + str(valeurStock)
            c.writelines(lineAdd)
            print str(dateCSV[0]) + ' ' + str(valeurStock)
        dateOld = dateCSV[0]
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
#calculValeurStock()
with open("actifStock.csv", "w") as c:
    principale(c)


