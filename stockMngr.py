import pyql
import csv, sys
import subprocess
import shlex
import subprocess
import platform
from collections import defaultdict

myAccount = None

class optionTransaction:
	uStockSymbol = None
	expiry = None
	strike = None
	isCall = False
	isPut = False
	sharesPerContract = None
	uOption = None
	quantity = None
	price = None
	date = None
	fees = None
	isBuy = False
	isSell = False
	expired = False
	exercized = False
	currency = None
	def __init__(self, uStockSymbol, expiry, strike, optionType, sharesPerContract, quantity, price, date, fees, transType, currency):
		self.uStockSymbol = uStockSymbol
		self.expiry = expiry
		self.strike = strike
		if(optionType=='Call'):
			self.isCall = True
		elif(optionType=='Put'):
			self.isPut = True
		self.sharesPerContract = sharesPerContract
		self.quantity = quantity
		self.price = price
		self.date = date
		self.fees = fees
		if(transType=='Buy'):
			self.isBuy = True
		elif(transType=='Sell'):
			self.isSell = True
		elif(transType=='Expire'):
			self.expired = True
		elif(transType=='Exercize'):
			self.exercized = True
		self.currency = currency

class stockTransaction:
	stockSymbol = None
	quantity = None
	price = None
	date = None
	fees = None
	currency = None
	isBuy = False
	isSell = False
	def __init__(self, symbol, quantity, price, date, fees, transtype, currency):
		self.stockSymbol = symbol
		self.quantity = quantity
		self.price = price
		self.date = date
		self.fees = fees
		if(transtype=='Buy'):
			self.isBuy = True
		elif(transtype=='Sell'):
			self.isSell = True
		self.currency = currency

class stockPosition:
	stockSymbol = None
	quantity = None
	price = None
	currency = None
	def __init__(self, symbol, quantity, price, currency):
		self.stockSymbol = symbol
		self.quantity = quantity
		self.price = price
		self.currency = currency

class currencyTransaction:
	uCurrencySell = None
	uCurrencyBuy = None
	date = None
	amountSold = None
	amountBought = None
	def __init__(self, uCurrencySell, uCurrencyBuy, date, amountSold, amountBought):
		self.uCurrencySell = uCurrencySell
		self.uCurrencyBuy = uCurrencyBuy
		self.date = date
		self.amountSold = amountSold
		self.amountBought = amountBought

class rebate:
	description = None
	date = None
	amount = None
	currency = None
	def __init__(self, description, date, amount, currency):
		self.description = description
		self.date = date
		self.amount = amount
		self.currency = currency

class cashTransfer:
	isDeposit = False
	isWithdrawal = False
	date = None
	amount = None
	currency = None
	def __init__(self, transType, date, amount, currency):
		if(transType=='Deposit'):
			self.isDeposit = True
		elif(transType=='Withdrawal'):
			self.isWithdrawal = True
		self.date = date
		self.amount = amount
		self.currency = currency

class dividendPayment:
	uStock = None
	dividendPerShare = None
	shareQuantity = None
	date = None
	dateRecord = None
	datePayment = None
	currency = None
	def __init__(self, uStock, date, dateRecord, datePayment, shareQuantity, dividendPerShare, currency):
		self.uStock = uStock
		self.date = date
		self.dateRecord = dateRecord
		self.datePayment = datePayment
		self.shareQuantity = shareQuantity
		self.dividendPerShare = dividendPerShare
		self.currency = currency

class account:
	stockTransDict = defaultdict(list)
	optionsTransDict = defaultdict(lambda : defaultdict(lambda : defaultdict(lambda : defaultdict(list))))
	currencyTransList = list()
	divTransDict = defaultdict(list)
	rebatesList = list()
	cashTransList = list()
	stockPosDict = defaultdict(list)
	optionPosDict = defaultdict(list)
#	openStockPosDict = defaultdict(list)
#	openOptionsPosDict = defaultdict(list)
#	closedStockPosDict = defaultdict(list)
#	closedOptionsTransDict = defaultdict(list)
#	totalRebates = None
#	totalDivPay = None
	def stockTrans2stockPos(self):
		for key, value in self.stockTransDict.iteritems():
			tempQuantity = 0
			tempPrice = 0
			for item in value:
				if(item.isBuy==True):
					tempPrice = ((tempQuantity*tempPrice)+(item.price*item.quantity))/(tempQuantity+item.quantity)
					tempQuantity += item.quantity
				elif(item.isSell==True):
					tempQuantity -= item.quantity
				else:
					print('Error malformed stock transaction item')
			print key + ' ' + str(tempQuantity) + ' ' + str(tempPrice) + ' ' + value[0].currency
			self.stockPosDict[key].append(stockPosition(key,tempQuantity,tempPrice,value[0].currency))

def readInData():
	with open('stocks.csv', 'rb') as csvfile:
		reader = csv.reader(csvfile)
		try:
			for row in reader:
					myAccount.stockTransDict[row[1]].append(stockTransaction(row[1],int(row[4]),float(row[5]),row[0],float(row[6]),row[3],row[2]))
		except csv.Error as e:
			sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))

	with open('options.csv', 'rb') as csvfile:
		reader = csv.reader(csvfile)
		try:
			for row in reader:
				myAccount.optionsTransDict[row[1]][row[4]][row[2]][row[3]].append(optionTransaction(row[1],row[4],row[3],row[2],row[8],row[7],row[9],row[0],row[10],row[6],row[5]))
		except csv.Error as e:
			sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))

	with open('currency.csv', 'rb') as csvfile:
		reader = csv.reader(csvfile)
		try:
			for row in reader:
				myAccount.currencyTransList.append(currencyTransaction(row[2],row[1],row[0],row[4],row[3]))
		except csv.Error as e:
			sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))

	with open('rebates.csv', 'rb') as csvfile:
		reader = csv.reader(csvfile)
		try:
			for row in reader:
				myAccount.rebatesList.append(rebate(row[1],row[0],row[2],row[3]))
		except csv.Error as e:
			sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))

	with open('dividends.csv', 'rb') as csvfile:
		reader = csv.reader(csvfile)
		try:
			for row in reader:
				myAccount.divTransDict[row[1]].append(dividendPayment(row[1],row[0],row[2],row[3],row[4],row[5],row[6]))
		except csv.Error as e:
			sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))

	with open('cash.csv', 'rb') as csvfile:
		reader = csv.reader(csvfile)
		try:
			for row in reader:
				myAccount.cashTransList.append(cashTransfer(row[1],row[0],row[2],row[3]))
		except csv.Error as e:
			sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))

def resizeTerminal():
	id_cmd='xdotool getactivewindow'
	resize_cmd='xdotool windowsize --usehints {id} 120 40'

	proc=subprocess.Popen(shlex.split(id_cmd),stdout=subprocess.PIPE)
	windowid,err=proc.communicate()
	proc=subprocess.Popen(shlex.split(resize_cmd.format(id=windowid)))
	proc.communicate()

def clear():
    subprocess.Popen( "cls" if platform.system() == "Windows" else "clear", shell=True)

if __name__ == "__main__":
	resizeTerminal()
	myAccount = account()
	readInData()
#	print(myAccount.stockTransDict.keys())
#	print(myAccount.stockTransDict['AMD'][0].date)
#	print(myAccount.stockTransDict['AMD'][1].date)
#	print(myAccount.optionsTransDict.keys())
#	print(myAccount.optionsTransDict['AMD'].keys())
#	print(myAccount.optionsTransDict['AMD']['10/27/13'].keys())
#	print(myAccount.currencyTransList[1].amountBought)
#	print(myAccount.rebatesList[1].amount)
#	print(myAccount.divTransDict['RY.TO'][0].dividendPerShare)
#	print(myAccount.cashTransList[0].amount)
	myAccount.stockTrans2stockPos()
