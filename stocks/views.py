from django.shortcuts import render, redirect
import requests
from django.db import connection
from django.http import JsonResponse
from datetime import datetime
from .models import Stocks
from members.decorators import allowed_users, run_once
from orders.models import Order
from django.contrib.auth.models import User
from django.contrib.sessions.backends.db import SessionStore

from django.contrib.auth.decorators import login_required

from bs4 import BeautifulSoup
from members.models import Member
from django.views.generic import View
from django.db.models import FloatField, Sum, F
from django.views.decorators.csrf import csrf_exempt


def count_profit(request, stock, current_value):
	#then = datetime.now()
	profit = 0
	previous_value = 0
	objects = Order.objects.filter(member=request.user.member).filter(stock = stock).filter(owned__gt=0).all()
	for obj in objects:
		previous_value += float(obj.owned*obj.purchase_price)
	#print(current_value, 'to ', previous_value)
	if(previous_value!=0):
		profit = round(((current_value - previous_value)/previous_value)*100,3)
	#print(datetime.now() - then)
	return profit

def stock_price(name):
	if(requests.get('https://www.bankier.pl/gielda/notowania/akcje')):
		url = requests.get('https://www.bankier.pl/gielda/notowania/akcje') 
		#file = open('C:/Users/grzes/OneDrive/Pulpit/akcje.html')
		soup = BeautifulSoup(url.content , 'html.parser')
		price = 0
		pb = soup.find("a", text=name).find_parent('tr')
		price = float(pb.select_one("td:nth-of-type(2)").text.strip().replace(',','.'))
		return price
	else:
		price = Stocks.objects.filter(name=name).get(price)
		return price


def update_stocks():
	if(requests.get('https://www.bankier.pl/gielda/notowania/akcje')):
		url = requests.get('https://www.bankier.pl/gielda/notowania/akcje')
		soup = BeautifulSoup(url.content, 'html.parser')
		#file = open('C:/Users/grzes/OneDrive/Pulpit/akcje.html')
		#soup = BeautifulSoup(file , 'html.parser')
		a = len(soup.find_all("tr", class_=False))
		while(a-1<Stocks.objects.count()):
			Stocks.objects.filter(id=Stocks.objects.count()).delete()
		tab = [[i] for i in range(a)]
		for i,record in enumerate(soup.find_all("tr", class_=False)):
			for data in record.findAll("td"):
				tab[i].append(data.text.strip())
			if(i>0):
				if(tab[i][1]=='LPP'):
					tab[i][2] = tab[i][2].replace(u'\xa0', u'')
					tab[i][7] = tab[i][7].replace(u'\xa0', u'')
					tab[i][8] = tab[i][8].replace(u'\xa0', u'')
					tab[i][9] = tab[i][9].replace(u'\xa0', u'')

				Stocks.objects.update_or_create(id=i, defaults={
					'name':tab[i][1],
					'price': float(tab[i][2].replace(',','.')),
					'change': float(tab[i][3].replace(',','.')),
					'perc': float(tab[i][4].replace(',','.').replace('%','')),
					'opening': float(tab[i][7].replace(',','.')),
					'max': float(tab[i][8].replace(',','.')),
					'min': float(tab[i][9].replace(',','.'))
					})

@csrf_exempt
def update(request):
	if request.method == 'POST':
		update_stocks()
		if(request.path=='/'):
			if(request.session['top'] == False):
				request.session['stocks'] = [entry for entry in Stocks.objects.order_by(request.session['order_by']).values()]
			else:
				request.session['stocks'] = [entry for entry in Stocks.objects.order_by('-'+request.session['order_by']).values()]
		elif(request.path=='/mystocks'):
			request.session['stocks'] = []
			for stock in request.session['bought_stocks']:
				request.session['stocks'].append([entry for entry in Stocks.objects.filter(name=stock).values()][0])
				
			if(request.session['top'] == False):
				request.session['stocks'] = sorted(request.session['stocks'], key=lambda k: k[request.session['order_by']])
			else:
				request.session['stocks'] = sorted(request.session['stocks'], key=lambda k: k[request.session['order_by']], reverse=True)
		return JsonResponse(data = {'stocks': request.session['stocks'], 'bought_stocks': request.session['bought_stocks']})


def get_bought_stocks(request):
	bought_stocks = {}
	orders = Order.objects.filter(member=request.user.member).filter(owned__gt=0).values('stock').distinct()
	print(orders)
	for order in orders:
		stock = Stocks.objects.get(id=order['stock'])
		suma = Order.objects.filter(member=request.user.member).filter(stock=stock).aggregate(Sum('owned'))
		bought_stocks.update({stock.name:{'value': round(stock.price*int(suma['owned__sum']),4), 'quantity': int(suma['owned__sum']), 'profit': 0}})
		bought_stocks[stock.name]['profit'] = count_profit(request, stock, bought_stocks[stock.name]['value'])
	return bought_stocks

def home(request):
	request.session['order_by'] = 'name'
	request.session['top'] = False
	request.session['stocks'] = [entry for entry in Stocks.objects.values()]

	if(request.user.is_authenticated):
		request.session['logged'] = True
		request.session['money'] = Member.objects.get(member=request.user).money
		request.session['bought_stocks'] = get_bought_stocks(request)
	else:
		if not 'logged' in request.session:
			request.session['logged'] = False
			request.session['money'] = 20000
			request.session['bought_stocks'] = {}


	data = {
		'stocks': request.session['stocks'],
		'money': request.session['money'],
		'bought_stocks': request.session['bought_stocks']
	}
	return render(request, 'stocks.html', data)

def my_stocks(request):
	request.session['order_by'] = 'name'
	request.session['top'] = False
	if(request.user.is_authenticated):
		request.session['money'] = Member.objects.get(member=request.user).money
		request.session['bought_stocks'] = get_bought_stocks(request)
	else:
		if not 'logged' in request.session:
			request.session['logged'] = False
			request.session['money'] = 20000
			request.session['bought_stocks'] = {}

	stocks=[]
	for value in request.session['bought_stocks']:
		stocks.append([entry for entry in Stocks.objects.filter(name=value).values()][0])
	
	request.session['stocks'] = stocks

	print(request.session['bought_stocks'])

	data = {
		'stocks': request.session['stocks'],
		'money': request.session['money'],
		'bought_stocks': request.session['bought_stocks']
	}

	return render(request, 'mystocks.html', data)

@login_required(login_url='login')
def top_users(request):
	user_data = {}

	members = Member.objects.filter(member__groups__name='customer').all()
	for ids, member in enumerate(members):
		money = Member.objects.get(name=member).money
		sum = 0
		orders = Order.objects.filter(member=member).filter(owned__gt=0).values('stock').distinct()
		for order in orders:
			stock = Stocks.objects.get(id=order['stock'])
			quantity = Order.objects.filter(member=member).filter(stock=stock).aggregate(Sum('owned'))
			sum += round(stock.price*int(quantity['owned__sum']),4)

		capital = money + sum
		member.capital = capital
		profit = round(((capital - 20000)/20000)*100,3)
		member.profit = profit
		member.save()


	data = {
	'money': Member.objects.get(member=request.user).money,
	'users': Member.objects.filter(member__groups__name='customer').all()
	}
	return render(request,'top_users.html', data)

@csrf_exempt
def order_table(request):
	if(request.method=='POST'):
		name = request.POST.get('name')
		request.session['order_by'] = name
		if(request.session['top'] == True):
			request.session['stocks'] = sorted(request.session['stocks'], key=lambda k: k[request.session['order_by']])
			request.session['top'] = False
		else:
			request.session['stocks'] = sorted(request.session['stocks'], key=lambda k: k[request.session['order_by']], reverse=True)
			request.session['top'] = True

		return JsonResponse({'stocks': request.session['stocks'], 'bought_stocks': request.session['bought_stocks']})

@login_required(login_url='login')
def charts(request,*args,**kwargs):
	data = {
		'money': Member.objects.get(member=request.user).money
	}
	return render(request,'charts.html', data)

def upd_charts(request):

	request.session['bought_stocks'] = get_bought_stocks(request)

	stocks=[]
	for value in request.session['bought_stocks']:
		stocks.append([entry for entry in Stocks.objects.filter(name=value).values()][0])

	labels = []
	values = []
	profits = []
	for stock in stocks:
		labels.append(stock['name'])
		values.append(request.session['bought_stocks'][stock['name']]['value'])
		profits.append(request.session['bought_stocks'][stock['name']]['profit'])

	return JsonResponse({'labels': labels, 'values': values, 'profits': profits})