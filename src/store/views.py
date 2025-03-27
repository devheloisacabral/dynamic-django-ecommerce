from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json


def get_cart_total(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
    return items, order

def store(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'store/store.html', context)

def cart(request):
    items, order = get_cart_total(request)
    context = {'items': items, 'order': order}
    return render(request, 'store/cart.html', context)

def get_cart_data(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}

    return JsonResponse({
        'get_cart_total': getattr(order, 'get_cart_total', 0),
        'get_cart_items': getattr(order, 'get_cart_items', 0)
    })


def checkout(request):
	context = {}
	return render(request, 'store/checkout.html', context)

def update_cart(request):
	data = json.loads(request.body)
	product_id = data['productId']
	action = data['action']

	customer = request.user.customer
	product = Product.objects.get(id=product_id)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	order_item, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		order_item.quantity = (order_item.quantity + 1)
	elif action == 'remove':
		order_item.quantity = (order_item.quantity - 1)

	order_item.save()

	if order_item.quantity <= 0:
		order_item.delete()

	return JsonResponse('Item was added', safe=False)