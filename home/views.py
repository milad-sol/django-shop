from django.shortcuts import render
from django.views import View
from product.models import Product

# Create your views here.
class HomeView(View):
	def get(self,request, *args, **kwargs):
		products = Product.objects.filter(available=True)
		return render(request, 'home/home.html', {'products':products})