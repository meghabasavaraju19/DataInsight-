from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_file, name='upload_file'),
    path('detail/<int:pk>', views.file_detail, name='file_detail'),
    path('file_list/', views.file_list, name='file_list'),
    path('delete_file/<int:pk>', views.delete_file, name='delete_file'),
    path('column_detail/<int:pk>/<str:colname>', views.column_detail, name='column_detail'),
    
]
