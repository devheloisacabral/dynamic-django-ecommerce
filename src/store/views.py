from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
import datetime
from .utils import cookie_cart, cart_data


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
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		data = cart_data(request)
		cookie_data = cookie_cart(request)
		items = data['items']
		order = data['order']
		cartItems = data['cartItems']

	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store/store.html', context)
def cart(request):

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		data = cart_data(request)
		cartItems = data['cartItems']
		order = data['order']
		items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
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
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		data = cart_data(request)
		cartItems = data['cartItems']
		order = data['order']
		items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
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
def process_order(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)

	else:
		name = data['form']['name']
		email = data['form']['email']

		cookieData = cookie_cart(request)
		items = cookieData['items']

		customer, created = Customer.objects.get_or_create(
				email=email,
				)
		customer.name = name
		customer.save()

		order = Order.objects.create(
			customer=customer,
			complete=False,
			)

		for item in items:
			product = Product.objects.get(id=item['id'])
			orderItem = OrderItem.objects.create(
				product=product,
				order=order,
				quantity=item['quantity'],
			)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)

	return JsonResponse('Payment submitted..', safe=False)


