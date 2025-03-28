from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
	path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	path('update_cart/', views.update_cart, name="update_cart"),
	path('get_cart_data/', views.get_cart_data, name='get_cart_data'),
	path('process_order/', views.process_order, name='process_order'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)