from django.shortcuts import render
import requests
from django.db import connection
from django.http import JsonResponse
from datetime import datetime
from .models import Stocks
from orders.models import Order
from django.contrib.sessions.backends.db import SessionStore

from bs4 import BeautifulSoup
from members.models import Member
from django.views.generic import View
from django.db.models import Sum
from django.views.decorators.csrf import csrf_exempt


def count_profit(request, ids):
	#then = datetime.now()
	profit = 0
	previous_value = 0
	current_value = request.session['bought_stocks'][ids]['value']
	objects = Order.objects.filter(stock_name = ids).filter(owned__gt=0).all()
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
		price = Stocks.objects.filter(name=name).first()
		print(price)


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
		if(request.session['main']==True):
			if(request.session['top'] == False):
				request.session['stocks'] = [entry for entry in Stocks.objects.order_by(request.session['order_by']).values()]
			else:
				request.session['stocks'] = [entry for entry in Stocks.objects.order_by('-'+request.session['order_by']).values()]
		else:
			request.session['stocks'] = []
			for stock_name in request.session['bought_stocks']:
				request.session['stocks'].append([entry for entry in Stocks.objects.filter(name=stock_name).values()][0])
				
			if(request.session['top'] == False):
				request.session['stocks'] = sorted(request.session['stocks'], key=lambda k: k[request.session['order_by']])
			else:
				request.session['stocks'] = sorted(request.session['stocks'], key=lambda k: k[request.session['order_by']], reverse=True)
		return JsonResponse(data = {'stocks': request.session['stocks'], 'bought_stocks': request.session['bought_stocks']})

def page(request):
	request.session['main']=True
	request.session['order_by'] = 'name'
	request.session['top'] = False
	update_stocks()
	request.session['stocks'] = [entry for entry in Stocks.objects.values()]
	request.session['bought_stocks'] = {}
	mem_id = 1
	mem = Member.objects.get(id=mem_id)

	vall = Order.objects.filter(member_id=mem_id).filter(owned__gt=0).values_list('stock_name', flat=True).distinct()
	for ids in vall:
		suma = Order.objects.filter(stock_name=ids).aggregate(Sum('owned'))
		price = Stocks.objects.filter(name=ids).values('price').first()['price']
		request.session['bought_stocks'].update({ids:{'value': round(price*int(suma['owned__sum']),3), 'quantity': int(suma['owned__sum']), 'profit': 0}})
		request.session['bought_stocks'][ids]['profit'] = count_profit(request, ids)

	data = {
		'stocks': request.session['stocks'],
		'money': Member.objects.get(id=1).money,
		'bought_stocks': request.session['bought_stocks']
	}
	return render(request, 'stocks.html', data)

def my_stocks(request):
	request.session['main']=False
	request.session['order_by'] = 'name'
	request.session['top'] = False
	names = []
	stocks = Stocks.objects.values()
	request.session['bought_stocks'] = {}
	request.session['stocks'] = []
	mem_id = 1
	mem = Member.objects.get(id=mem_id)

	vall = Order.objects.filter(member_id=mem_id).filter(owned__gt=0).values_list('stock_name', flat=True).distinct()
	for name in vall:
		suma = Order.objects.filter(stock_name=name).aggregate(Sum('owned'))
		price = Stocks.objects.filter(name=name).values('price').first()['price']
		request.session['bought_stocks'].update({name:{'value': round(price*int(suma['owned__sum']),3), 'quantity': int(suma['owned__sum']), 'profit': 0}})
		request.session['bought_stocks'][name]['profit'] = count_profit(request, name)
		names.append(name)

	stocks = []
	names.sort()
	for value in names:
		request.session['stocks'].append([entry for entry in Stocks.objects.filter(name=value).values()][0])

	data = {
		'stocks': request.session['stocks'],
		'money': Member.objects.get(id=1).money,
		'bought_stocks': request.session['bought_stocks']
	}

	return render(request, 'mystocks.html', data)

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

def charts(request,*args,**kwargs):
	data = {
		'money': Member.objects.get(id=1).money
	}
	return render(request,'charts.html', data)

def upd_charts(request):
	mem_id = 1
	mem = Member.objects.get(id=mem_id)
	stocks = Stocks.objects.values()

	vall = Order.objects.filter(member_id=mem_id).filter(owned__gt=0).values_list('stock_name', flat=True).distinct()
	for name in vall:
		suma = Order.objects.filter(stock_name=name).aggregate(Sum('owned'))
		price = Stocks.objects.filter(name=name).values('price').first()['price']
		request.session['bought_stocks'].update({name:{'value': round(price*int(suma['owned__sum']),3), 'quantity': int(suma['owned__sum']), 'profit': 0}})
		request.session['bought_stocks'][name]['profit'] = count_profit(request, name)

	stocks=[]
	for value in request.session['bought_stocks']:
		print(value)
		stocks.append([entry for entry in Stocks.objects.filter(name=value).values()][0])

	labels = []
	values = []
	profits = []
	for stock in stocks:
		labels.append(stock['name'])
		values.append(request.session['bought_stocks'][stock['name']]['value'])
		profits.append(request.session['bought_stocks'][stock['name']]['profit'])

	return JsonResponse({'labels': labels, 'values': values, 'profits': profits})