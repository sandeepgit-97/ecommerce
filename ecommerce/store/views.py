from django.shortcuts import render,get_object_or_404
from .models import *
from django.http import JsonResponse
import json
import datetime
from .models import Product
from .utils import cookieCart,cartData,guestOrder
# Create your views here.
def updateItem(request):
    if request.method != 'POST':
        return JsonResponse('Invalid request', safe=False)

    if not request.user.is_authenticated:
        return JsonResponse('User not logged in', safe=False)

    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    customer = request.user.customer
    product = Product.objects.filter(id=productId).first()

    if not product:
        return JsonResponse('Product not found', safe=False)

    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1

    orderItem.save() 

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item updated', safe=False)

def Store(request):
    cookieCart = cartData(request)
    cartItems = cookieCart['cartItems']
    order = cookieCart['order']
    items = cookieCart['items']
        
    product=Product.objects.all()
    context={'products':product, 'order':order, 'items':items, 'cartItems': cartItems}
    return render(request,'Store.html',context)

def Cart(request):
    cookieCart = cartData(request)
    cartItems = cookieCart['cartItems']
    order = cookieCart['order']
    items = cookieCart['items']
    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'Cart.html', context)



def Checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    context = {'Orderitems': items, 'order': order, 'items': items}
    return render(request, 'Checkout.html', context)

def ProcessOrder(request):
    if request.method != 'POST':
        return JsonResponse('Invaid request', safe=False)
    transaction_id = datetime.datetime.now().timestamp()
    data=json.loads(request.body)
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
       
    else:
        customer, order = guestOrder(request, data)
        
        total = float(data['form']['total'])
        order.transaction_id = transaction_id
        
        if total == order.get_cart_total:
            order.complete = True
        order.save()
        
        if order.shipping == True:
            Shipping_Address.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )
            
    return JsonResponse('Payment Submitted..', safe=False)

def product_view(request, pk):
    product = get_object_or_404(Product, id=pk)
    
    cartItems = 0 
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cartItems = order.get_cart_items

    context = {'product': product, 'cartItems': cartItems}
    return render(request, 'view.html', context) 

def Main(request):
    return render(request, 'Main.html')

    