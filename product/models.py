from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    sub_category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                                     related_name='sub_categories')
    is_sub_category = models.BooleanField(default=False)

    class Meta:
        ordering = ['name']

        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('home:home_category', args=[self.slug, ])


class Product(models.Model):
    category = models.ManyToManyField(Category, related_name='products')
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    image = models.ImageField()
    description = RichTextField()
    price = models.IntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # ایجاد URL برای هر پست با استفاده از slug
        return reverse('product:product_detail', kwargs={
            'slug': self.slug
        })
