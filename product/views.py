from django.shortcuts import render, get_object_or_404
from django.views import View
from orders.forms import CartAddForm
from product.models import Product


class ProductDetailView(View):
    def get(self, request, *args, **kwargs):
        product = get_object_or_404(Product, slug=self.kwargs['slug'])
        form = CartAddForm()

        return render(request, 'product/product_detail.html', {'product': product, 'form': form})


