###
from django.shortcuts import render, HttpResponse, redirect
from .models import Quote
from apps.login_app.models import User
from django.contrib import messages

def index(request):
    if 'user_id' in request.session:
        quotes = Quote.objects.all()
        user = User.objects.get(id = request.session['user_id'])
        context = {
            'quotes': quotes,
            'user':user,
        }
        return render(request, "belt_app/index.html", context)
    else:
        return redirect("/")

def quote_add(request):
    if 'user_id' in request.session:
        errors = Quote.objects.basic_validator(request.POST)
        
        if len(errors)>0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/quotes")
        else:

            user = User.objects.get(id = request.session['user_id'])
            
            Quote.objects.create(author = request.POST['author'], quote = request.POST['quote'],  user = user)
            
            return redirect("/quotes")
    else:
        return redirect("/")

def quote_like(request):
    if 'user_id' in request.session:
        user = User.objects.get(id = request.session['user_id'])
        quote = Quote.objects.get(id = request.POST['quote_id'])
        quote.likes.add(user)
        return redirect("/quotes")
    else:
        return redirect("/")

def quote_delete(request):
    if 'user_id' in request.session:
        
        quote = Quote.objects.get(id = request.POST['quote_id'])
        if quote.user.id == request.session['user_id']:
            quote.delete()
        
        return redirect("/quotes")
    else:
        return redirect("/")

def quote_user(request, user_id):
    if 'user_id' in request.session:
        quotes = Quote.objects.filter(user = user_id)
        user = User.objects.get(id = user_id)
        context = {
            'quotes': quotes,
            'user': user,
        }
        return render(request, "belt_app/user.html", context)
    else:
        return redirect("/")
    return HttpResponse("yo")
