from django.shortcuts import render, redirect
from .models import User, Size, Topping, Pizza
from django.contrib import messages
import bcrypt
# Create your views here.

def addcart(request, pizzaId):
    return redirect ('/createPizza')


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
    # Pizza object needs to be created first with id to set toppings
    toppings = request.POST.getlist('toppings')
    print(toppings)
    pizza.toppings.set(toppings)
    # once order model is set and addcart view is established, return redirect to "/addcart"

    return redirect('/createPizza')

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
    context = {
        'user': User.objects.get(id=request.session['user_id']),
        'size': Size.objects.all(),
        'toppings':Topping.objects.all()
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
    }
    return render(request, "account.html", context)
