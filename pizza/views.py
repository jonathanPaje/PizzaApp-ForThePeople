from django.shortcuts import render, redirect
from .models import User, Size, Topping, Pizza, Order
from django.http import JsonResponse
from django.contrib import messages
from decimal import *
from random import randint
import bcrypt
import json
# Create your views here.

# TODO LIST
# implement stripe payment
# create favorite button in account page
#create remove button in order page
# render a list of favorites page

def paymentComplete(request):
    body = json.loads(request.body)
    print ('BODY:', body)
    del request.session['cart_id']
    return JsonResponse('Payment completed!', safe=False)

def surpriseMe(request):
    value = randint(1, 4)
    pizza = Pizza.objects.get(id=value)
    return redirect(f'/addcart/{pizza.id}')

def order(request):
    user = User.objects.get(id=request.session['user_id'])
    cart = Order.objects.get(id = request.session['cart_id'])
    context = {
        'user': user,
        'cart':cart
    }
    return render (request, "order.html",context)

def addcart(request, pizza_id):
    if 'user_id' not in request.session:
        messages.error(request, "You need to register or log in!")
        return redirect('/')
    if 'cart_id' not in request.session:        
        user = User.objects.get(id=request.session['user_id'])
        cart = Order.objects.create(
            order_user = user
        )
        request.session['cart_id'] = cart.id
    cart=Order.objects.get(id=request.session['cart_id'])
    pizza = Pizza.objects.get(id = pizza_id)
    cart.order_item.add(pizza)
    total = Decimal(cart.order_price) + pizza.size.price
    cart.order_price = total
    cart.save()
    return redirect ('/order')


def makepizza(request):
    if 'user_id' not in request.session:
        messages.error(request, "You need to register or log in!")
        return redirect('/')
    if request.method == "GET":
        return redirect('/home')
    user = User.objects.get(id = request.session['user_id'])

    pizza = Pizza.objects.create(
        created_by = user,
        size = Size.objects.get(id= request.POST['size']),
        name = request.POST['name']
    )

    toppings = request.POST.getlist('toppings')
    print(toppings)
    pizza.toppings.set(toppings)

    return redirect(f'/addcart/{pizza.id}')

def createPizzaPage(request):
    if 'user_id' not in request.session:
        messages.error(request, "You need to register or log in!")
        return redirect('/')
    context = {
        'user': User.objects.get(id=request.session['user_id']),
        'size': Size.objects.all(),
        'toppings':Topping.objects.all()
    }
    return render(request, "createPizzaPage.html", context)

def index(request):
    return render(request, "index.html")

def register(request):
    if request.method =="POST":
        errors = User.objects.create_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
            user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=hashed_pw)
            request.session['user_id'] = user.id
            return redirect('/success')
            
    return redirect('/')

def login(request):
    user = User.objects.filter(email=request.POST['email'])
    if len(user) > 0:
        user = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
            request.session['user_id'] = user.id
            return redirect('/success')
    messages.error(request, "Email or Password is incorrect")
    return redirect('/')

def success(request):
    if 'user_id' not in request.session:
        messages.error(request, "You need to register or log in!")
        return redirect('/')
    if 'cart_id' not in request.session:        
        user = User.objects.get(id=request.session['user_id'])
        cart = Order.objects.create(
            order_user = user
        )
        request.session['cart_id'] = cart.id
    context = {
        'user': User.objects.get(id=request.session['user_id']),
        'cart': Order.objects.get(id=request.session['cart_id']),
    }
    return render(request, "success.html", context)

def logout(request):
    request.session.clear()
    return redirect('/')
    
def account(request):
    if 'user_id' not in request.session:
        messages.error(request, "You need to register or log in!")
        return redirect('/')
    context = {
        'user': User.objects.get(id=request.session['user_id']),
        'cart': Order.objects.get(id=request.session['cart_id']),
    }
    return render(request, "account.html", context)
