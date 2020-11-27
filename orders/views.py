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

@csrf_exempt
def process(request):
	if request.method == 'POST':
		x = request.POST.get('quantity')
		if(is_number(x)):
			stock = Stocks.objects.get(name=request.POST.get('name'))
			quantity = int(x)
			price = stock_price(stock.name)
			bought_stocks = request.session['bought_stocks']

			if(request.user.is_authenticated):
				if(request.POST.get('buy')=='true'):
					print('buy')
					maximum = int(member.money/price)
					
					if(maximum!=0):
						if(quantity>maximum):
							quantity=maximum
					else:
						return JsonResponse({'money': member.money, 'quantity' : 'no money', 'value' : 0, 'profit': 0})

					member.money -= quantity*price
					member.money = round(member.money,4)
					member.save()
					Order.objects.create(
							member = request.user.member,
							stock = stock,
							quantity = quantity,
							owned = quantity,
							purchase_price = price,
							buy = bool(request.POST.get('buy'))
							)

					if stock.name in bought_stocks:
						befor_quantity = int(bought_stocks[stock.name]['quantity'])
						after_quantity = befor_quantity + quantity
						print(befor_quantity, quantity)
					else:
						after_quantity = quantity

					bought_stocks.update({stock.name:{'value':  round(price * after_quantity,3), 'quantity': after_quantity, 'profit': 0}})
					bought_stocks[stock.name]['profit'] = count_profit(request, stock, bought_stocks[stock.name]['value'])

					request.session['bought_stocks'] = bought_stocks

					return JsonResponse({'money': member.money, 'quantity' : after_quantity, 'value' : round(price * after_quantity,3), 'profit': bought_stocks[stock.name]['profit']})
				
				elif(request.POST.get('buy')=='false'):
					print('sell')
					orders = Order.objects.filter(member=request.user.member).filter(owned__gt=0).all()
					sold = 0

					while(Order.objects.filter(member=request.user.member).filter(stock = stock).filter(owned__gt=0).first()):
						obj = Order.objects.filter(member=request.user.member).filter(stock = stock).filter(owned__gt=0).first()
						
						if(quantity>=obj.owned):
							quantity -= obj.owned
							sold += obj.owned
							member.money += obj.owned*price
							member.save()
							obj.owned = 0
							obj.save()

						else:
							sold += quantity
							member.money += quantity*price
							member.save()
							obj.owned = obj.owned - quantity
							obj.save()
							break
					if(Order.objects.filter(member=request.user.member).filter(stock = stock).filter(owned__gt=0).first()):
						owned = int(bought_stocks[stock.name]['quantity'])
						bought_stocks.update({stock.name:{'value':  round(price * (owned - sold), 3), 'quantity': owned - sold, 'profit': 0}})
						bought_stocks[stock.name]['profit'] = count_profit(request, stock, bought_stocks[stock.name]['value'])
						value = bought_stocks[stock.name]['value'] - price * quantity
						request.session['bought_stocks'] = bought_stocks
						return JsonResponse({'money': round(member.money,4), 'quantity' : bought_stocks[stock.name]['quantity'], 'value' : round(float(value),3), 'profit': bought_stocks[stock.name]['profit']})
					
					else:
						bought_stocks.pop(stock.name)
						request.session['bought_stocks'] = bought_stocks
						return JsonResponse({'money': round(member.money,4), 'quantity' : 0, 'value' : 0, 'profit': 0})
					
			else:

				if(request.POST.get('buy')=='true'):
					print('buy')
					money = request.session['money']
					maximum = int(money/price)

					if(maximum!=0):
						if(quantity>maximum):
							quantity=maximum
					else:
						return JsonResponse({'money': money, 'quantity' : 'no money', 'value' : 0, 'profit': 0})

					money -= quantity*price
					money = round(money,4)

					if stock.name in bought_stocks:
						befor_quantity = int(bought_stocks[stock.name]['quantity'])
						after_quantity = befor_quantity + quantity
					else:
						after_quantity = quantity

					bought_stocks.update({stock.name:{'value':  round(price * after_quantity,3), 'quantity': after_quantity, 'profit': 0}})
					request.session['bought_stocks'] = bought_stocks
					request.session['money'] = money
					return JsonResponse({'money': money, 'quantity' : after_quantity, 'value' : round(price * after_quantity,3), 'profit': 0})
				
				else:
					print('sell')
					if stock.name in bought_stocks:
						if(quantity>=bought_stocks[stock.name]['quantity']):
							money += price*int(bought_stocks[stock.name]['quantity'])
							bought_stocks.pop(stock.name)
							request.session['money'] = money
							return JsonResponse({'money': money, 'quantity' : 0, 'value' : 0, 'profit': 0})
						else:
							money += price*quantity
							bought_stocks[stock.name]['quantity'] -= quantity
							request.session['money'] = money
							return JsonResponse({'money': money, 'quantity' : bought_stocks[stock.name]['quantity'], 'value' : bought_stocks[stock.name]['quantity']*price, 'profit': 0})
					else:
						return JsonResponse({'money': money, 'quantity' : 0, 'value' : 0, 'profit': 0})

				member = Member.objects.get(member=request.user)

				
