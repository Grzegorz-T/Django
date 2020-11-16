from django.shortcuts import render
from .models import Order
from members.models import Member
from stocks.models import Stocks
from stocks.views import stock_price, count_profit

from django.http import JsonResponse
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt

def is_number(n):
    try:
        int(n)
        return True
    except ValueError:
        return  False

def bought_st():
	a = Stocks.objects.all()
	for j,item in enumerate(a): #zapis do pamięci
		b = Orders.objects.with_entities(func.sum(Orders.owned).label("mySum")).filter_by(stock_id=item['id']).first()
		if(b.mySum):
			Bought.bought_stocks.update({item['id']:{'quantity': int(b.mySum), 'value': round(item['price']*int(b.mySum),3), 'profit': 0}})
			Bought.bought_stocks[item['id']]['profit'] = count_profit(item['id'])


@csrf_exempt
def process(request):
	if request.method == 'POST':
		x = request.POST.get('quantity')
		if(is_number(x)):
			mem_id = 1
			mem = Member.objects.get(id=mem_id)
			stock_id = Stocks.objects.filter(id=request.POST.get('id')).values('name').first()['name']
			quantity = int(x)
			price = stock_price(stock_id)
			bought_stocks = request.session['bought_stocks']

			if(request.POST.get('buy')=='true'):
				print('buy')
				maximum = int(mem.money/price)
				if(maximum!=0):
					if(quantity>maximum):
						quantity=maximum
				else:
					return JsonResponse({'money': mem.money, 'quantity' : 'no money', 'value' : 0, 'profit': 0})

				mem.money -= quantity*price
				mem.money = round(mem.money,3)
				mem.save()
				Order.objects.create(
						member_id = mem_id,
						stock_name = stock_id,
						quantity = quantity,
						owned = quantity,
						stock_id = 5,
						purchase_price = price,
						buy = bool(request.POST.get('buy'))
						)

				if stock_id in bought_stocks:
					befor_quantity = int(bought_stocks[stock_id]['quantity'])
					after_quantity = befor_quantity + quantity
					print(befor_quantity, quantity)
				else:
					after_quantity = quantity

				bought_stocks.update({stock_id:{'value':  round(price * after_quantity,3), 'quantity': after_quantity, 'profit': 0}})
				bought_stocks[stock_id]['profit'] = count_profit(request, stock_id)

				request.session['bought_stocks'] = bought_stocks

				return JsonResponse({'money': mem.money, 'quantity' : after_quantity, 'value' : round(price * after_quantity,3), 'profit': bought_stocks[stock_id]['profit']})
			
			elif(request.POST.get('buy')=='false'):
				print('sell')
				orders = Order.objects.filter(member_id=mem_id).filter(owned__gt=0).all()
				sold = 0
				while(Order.objects.filter(stock_id = stock_id).filter(owned__gt=0).first()):
					obj = Order.objects.filter(stock_id = stock_id).filter(owned__gt=0).first()
					if(quantity>=obj.owned):
						quantity -= obj.owned
						sold += obj.owned
						mem.money += obj.owned*price
						mem.save()
						obj.owned = 0
						obj.save()

					else:
						sold += quantity
						mem.money += quantity*price
						mem.save()
						obj.owned = obj.owned - quantity
						obj.save()
						break

				if(Order.objects.filter(stock_id = stock_id).filter(owned__gt=0).first()):
					owned = int(bought_stocks[stock_id]['quantity'])
					bought_stocks.update({stock_id:{'value':  round(price * (owned - sold), 3), 'quantity': owned - sold, 'profit': 0}})
					bought_stocks[stock_id]['profit'] = count_profit(request, stock_id)
					value = bought_stocks[stock_id]['value'] - price * quantity
					request.session['bought_stocks'] = bought_stocks
					return JsonResponse({'money': round(mem.money,3), 'quantity' : bought_stocks[stock_id]['quantity'], 'value' : round(float(value),3), 'profit': bought_stocks[stock_id]['profit']})
				
				else:
					bought_stocks.pop(stock_id)
					request.session['bought_stocks'] = bought_stocks
					return JsonResponse({'money': round(mem.money,3), 'quantity' : 0, 'value' : 0, 'profit': 0})
					
