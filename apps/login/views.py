from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages
import bcrypt
# LOGIN/REGISTER
def index(request): 
    return render(request,'login/index.html')

def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], password = password)
        request.session['user_id'] = User.objects.get(email = request.POST['email']).id
        return redirect('/wishes') #THE ROUTE THAT LEADS TO INDEX OF APP TWO

def login(request): 
    errors = User.objects.login_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        request.session['user_id'] = User.objects.get(email = request.POST['email']).id
        return redirect('/wishes') #THE ROUTE THAT LEADS TO INDEX OF APP TWO


def logout(request):
    del request.session['user_id']
    return redirect('/')

#WISH SECTION
def wishes(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user_id = request.session['user_id']
    user = User.objects.get(id = user_id)
    context = {
        'wishes' : Wish.objects.filter(wisher = user).exclude(granter__isnull=False),
        'grantedlike' : Wish.objects.all().exclude(granter__isnull=True).exclude(wisher = user),
        'grantednolike' : Wish.objects.all().exclude(granter__isnull=True).filter(wisher = user),
        'first_name' : user.first_name,
    }
    return render(request,'login/home.html', context)

def edit(request,id):
    if 'user_id' not in request.session:
        return redirect('/')
    user_id = request.session['user_id']
    user = User.objects.get(id = user_id)
    wish = Wish.objects.get(id = id)
    context = {
        'first_name' : user.first_name,
        'name' : wish.name,
        'desc' : wish.desc,
        'wish_id': wish.id,
    }
    print(context)
    return render(request,'login/edit.html', context)

def update(request):
    if 'user_id' not in request.session:
        return redirect('/')
    errors = Wish.objects.wish_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/wishes/new')
    else:
        wish = Wish.objects.get(id = request.POST['wish_id'])
        wish.name = request.POST['name']
        wish.desc = request.POST['desc'] 
        wish.save()
        return redirect("/wishes")

def new(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user_id = request.session['user_id']
    user = User.objects.get(id = user_id)
    context = {
        'first_name' : user.first_name,
    }
    return render(request,'login/new.html', context)

def add(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user_id = request.session['user_id']
    user = User.objects.get(id = user_id)
    errors = Wish.objects.wish_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/wishes/new')
    else:
        Wish.objects.create(name = request.POST['name'], desc = request.POST['desc'], wisher = user)
        return redirect('/wishes')

def grant(request,id):
    if 'user_id' not in request.session:
        return redirect('/')
    user_id = request.session['user_id']
    user = User.objects.get(id = user_id)
    wish = Wish.objects.get(id = id)
    wish.granter = user
    wish.save()
    return redirect('/wishes')

def like(request,id):
    if 'user_id' not in request.session:
        return redirect('/')
    user_id = request.session['user_id']
    user = User.objects.get(id = user_id)
    wish = Wish.objects.get(id = id)
    errors = {}
    if len(Like.objects.filter(user = user).filter(wish = wish)) > 0:
        errors["user"] = "Already liked by you glad you really like it though!"
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/wishes')
    else:
        Like.objects.create(wish = wish, user = user)
        return redirect('/wishes')

def stats(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user_id = request.session['user_id']
    user = User.objects.get(id = user_id)
    context = {
        'pendinguserwishes' : Wish.objects.filter(wisher = user).exclude(granter__isnull=True),
        'granteduserwishes' : Wish.objects.filter(wisher = user).exclude(granter__isnull=False),
        'grantedwishes' : Wish.objects.all().filter(granter__isnull=False),
        'first_name' : user.first_name,
    }
    return render(request,'login/stats.html', context)

def delete(request,id):
    if 'user_id' not in request.session:
        return redirect('/')
    Wish.objects.filter(id = id).delete()
    return redirect('/wishes')