from django.shortcuts import render
from django.views import View

from product.models import Product
from .tasks import all_bucket_objects_task ,delete_bucket_objects_task


# Create your views here.
class HomeView(View):
    def get(self, request, *args, **kwargs):
        products = Product.objects.filter(available=True)
        return render(request, 'home/home.html', {'products': products})


class BucketHome(View):
    template_name = 'home/bucket.html'

    def get(self, request, *args, **kwargs):
        objects = all_bucket_objects_task()
        return render(request, self.template_name, {'objects': objects})

