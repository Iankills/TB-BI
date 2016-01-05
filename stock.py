import csv
import string

fname = "WalletTransactions.csv"
file = open(fname, "rb")

reader = csv.reader(file)

listProductString = list()
listProductObject = list()

for line in reader:
        vararecup = line[0].split(' ', 1)
        listProductString.append(line[3])
        listProductStringSet = list(set(listProductString))
        listProductStringSet.sort()
        print listProductStringSet

for lineProduct in listProductStringSet:
    print lineProduct
    lineProduct = list()
    listProductObject.append(lineProduct)

print listProductObject.__len__()

class Product:

    def __init__(self, productName):
        self.productName = productName
