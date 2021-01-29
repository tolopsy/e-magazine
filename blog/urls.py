from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name='home'),
	path('post/<slug:post_slug>/<int:year>/<int:month>/<int:day>/', views.post_detail, name='detail'),
	path('category/<slug:slug>/', views.category, name='category'),
	path('contact/', views.contact, name='contact'),
	path('search/', views.search, name='search'),
	path('privacy-policy/', views.privacy, name='privacy'),
	path('newsmail/', views.newsmail, name='newsmail'),
	path('unsubscribe/<uuid:code>/', views.unsubscribe, name='unsubscribe'),
]