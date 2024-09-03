from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('product/<int:pk>', views.product, name="product"),
    path('category/<str:foo>', views.category, name="category"),
    path('category_summary/', views.category_summary, name="category_summary"),
    path('search/', views.search, name='search'),
]

