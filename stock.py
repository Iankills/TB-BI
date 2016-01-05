# coding=utf-8
import csv

# Ouverture du flux
file = open("WalletTransactions.csv", "rb")

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
    reader = csv.reader(file)
    listProductString = list()
    listProductObject = list()
    dictProduct = {}

    for line in reader:
        # print line[3]
        if testDictProduct(dictProduct, line[3]):
            continue
        else:
            dictProduct.update({line[3]: [line[0], line[], line[], line[], line[]]})

    print dictProduct
    print dictProduct.__len__()


# test pour la création du stock initial
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