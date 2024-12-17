from django.contrib import messages
from utils import IsAdminUserMixin
from django.shortcuts import render, redirect
from django.views import View

from product.models import Product, Category
from . import tasks
from .forms import BucketUploadForm


# Create your views here.
class HomeView(View):
    def get(self, request, slug=None):
        products = Product.objects.filter(available=True)
        categories = Category.objects.all()
        if slug:
            products = products.filter(category__slug=slug)
        return render(request, 'home/home.html', {'products': products, 'categories': categories})


class BucketHome(IsAdminUserMixin, View):
    template_name = 'home/bucket.html'

    def get(self, request, *args, **kwargs):
        objects = tasks.all_bucket_objects_task()
        return render(request, self.template_name, {'objects': objects})


class DeleteBucketObj(IsAdminUserMixin, View):
    def get(self, request, key):
        result = tasks.delete_object_task.delay(key
                                                )
        messages.success(request, 'Task deleted', 'info')
        return redirect("home:bucket")


class DownloadBucketObj(IsAdminUserMixin, View):
    def get(self, request, key):
        tasks.download_object_task.delay(key)
        messages.success(request, 'your download will start soon', 'info')
        return redirect("home:bucket")


class UploadBucketObj(IsAdminUserMixin, View):
    form_class = BucketUploadForm
    template_name = 'home/upload_bucket.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)  # Include request.FILES
        if form.is_valid():
            image = form.cleaned_data['image']
            filename = image.name
            tasks.upload_object_task.delay(image.read(), filename)
            messages.success(request, 'Your file has been uploaded', 'info')
            return redirect("home:bucket")
        return render(request, self.template_name, {'form': form})
