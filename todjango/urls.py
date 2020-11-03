"""todjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from stocks.views import page, my_stocks, charts, update, upd_charts, order_table
from orders.views import process

urlpatterns = [
    path('', page, name='page'),
    path('mystocks/', my_stocks, name='my_stocks'),
    path('charts/', charts, name='charts'),
    path('process/', process),
    path('admin/', admin.site.urls),
    path('_update/', update),
    path('_upd_charts/', upd_charts),
    
    path('order_table/', order_table),
    
    
]
