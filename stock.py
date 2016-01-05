import csv
import string

#### Ouverture du csv ####
fname = "WalletTransactions.csv"
file = open(fname, "rb")

#### Classe Produit ####
class Product:
    def __init__(self, nameProduct):
        self.nameProduct = nameProduct
        self.listInstanceProduct = list()

def sortAndCreateListProductObject():
    reader = csv.reader(file)
    listProductString = list()
    listProductObject = list()

    for line in reader:
        vararecup = line[0].split(' ', 1)
        listProductString.append(line[3])
        listProductStringSet = list(set(listProductString))
        listProductStringSet.sort()
        #print listProductStringSet

    for lineProduct in listProductStringSet:
        #print lineProduct
        listProductObject.append(lineProduct)

    print listProductObject
    print listProductObject.__len__()


def addStock():
    reader = csv.reader(file)
    listProductString = list()
    listProductObject = list()
    dictProduct = {}

    for line in reader:
        print line[3]

addStock()








