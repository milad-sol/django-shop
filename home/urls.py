from django.urls import path
from . import views


app_name = 'home'

urlpatterns = [
    path('',views.HomeView.as_view(),name='home'),
    path('bucket/',views.BucketHome.as_view(),name='bucket'),
    path('delete_bucket/<key>/',views.DeleteBucketObj.as_view(),name='delete_obj_bucket'),

]