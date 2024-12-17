from django.urls import path, include

from . import views

app_name = 'home'

bucket_urls = [
    path('', views.BucketHome.as_view(), name='bucket'),
    path('delete_obj/<key>/', views.DeleteBucketObj.as_view(), name='delete_obj_bucket'),
    path('download_obj/<str:key>', views.DownloadBucketObj.as_view(), name='download_obj_bucket'),
    path('upload_obj/', views.UploadBucketObj.as_view(), name='upload_obj_bucket'),

]

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
   path('category/<slug:slug>/',views.HomeView.as_view(), name='home_category'),
    path('bucket/', include(bucket_urls)),

]
