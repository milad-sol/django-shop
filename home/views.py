from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from . import tasks
from product.models import Product


# Create your views here.
class HomeView(View):
    def get(self, request, *args, **kwargs):
        products = Product.objects.filter(available=True)
        return render(request, 'home/home.html', {'products': products})


class BucketHome(View):
    template_name = 'home/bucket.html'

    def get(self, request, *args, **kwargs):
        objects = tasks.all_bucket_objects_task()
        return render(request, self.template_name, {'objects': objects})


class DeleteBucketObj(View):
    def get(self, request,key):
       result = tasks.delete_object_task.delay(key
       )
       messages.success(request, 'Task deleted','info')
       return redirect("home:bucket")

