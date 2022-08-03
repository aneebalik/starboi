from django.urls import path
from . import views

urlpatterns = [
    path('blog/', views.blog_page, name='blog_page'),
    path('<slug:slug>/', views.blog_details, name='blog_details'),
]
