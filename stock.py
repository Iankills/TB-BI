# coding=utf-8
import csv

# Ouverture du flux
fileWalletTransaction = open("WalletTransactions.csv", "rb")
fileStockInitial = open("stock_initial.csv", "rb")

# Cette méthode ne sert à rien mais je la laisse pour une éventualité
def sortAndCreateListProductObject():
    reader = csv.reader(file)
    listProductString = list()
    listProductObject = list()

    for line in reader:
        listProductString.append(line[3])
        listProductStringSet = list(set(listProductString))
        listProductStringSet.sort()

    for lineProduct in listProductStringSet:
        listProductObject.append(lineProduct)

    print listProductObject
    print listProductObject.__len__()


# Creation du stock initial avec tous les produits
def createInitialStock():
    readerWalletT = csv.reader(fileWalletTransaction)
    readerStockInitial = csv.reader(fileStockInitial)
    dictProduct = {}

    for line in readerWalletT:
        if testDictProduct(dictProduct, line[3]):
            continue
        else:
            dictProduct.update({line[3]: []})
            #dictProduct.update({line[3]: [line[0], line[2], line[4]]})
    for line in readerStockInitial:
        if testDictProduct(dictProduct, line[3]):
            continue
        else:
            dictProduct.update({line[3]: []})

    print dictProduct
    print dictProduct.__len__()

def updateSotck():

    print "ok"

#test pour la création du stock initial
def testDictProduct(dictProduct, product):
    for mot in dictProduct:
        if mot == product:
            return True
        else:
            return False

# le main
createInitialStock()
# fermeture du flux
file.close()