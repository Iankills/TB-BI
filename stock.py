# coding=utf-8
import csv

# Ouverture du csv
fname = "WalletTransactions.csv"
file = open(fname, "rb")


# Cette méthode ne sert à rien mais je la laisse pour peut être plus tard
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


# Creation du stock initial avec tout les produits
def createInitialStock():
    reader = csv.reader(file)
    listProductString = list()
    listProductObject = list()
    dictProduct = {}

    for line in reader:
        # print line[3]
        if testDictProduct(dictProduct, line[3]):
            continue
        else:
            dictProduct.update({line[3]: []})

    print dictProduct
    print dictProduct.__len__()


# test pour la création du stock initial
def testDictProduct(dictProduct, product):
    for mot in dictProduct:
        if mot == product:
            return True
        else:
            return False

#le main
createInitialStock()
