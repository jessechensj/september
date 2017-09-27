from django.shortcuts import render, HttpResponse, redirect
from django.contrib.sessions.models import Session
from models import User, Travelplan
from django.contrib import messages
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

def index(request):
  return render(request, 'index.html')

def login(request):
  if request.method == "POST":
    if re.match(EMAIL_REGEX, request.POST['email']) != None:
      user = User.objects.filter(email=request.POST['email'])
      if user:
        if user[0].password == request.POST["password"]:
          request.session['user_id'] = user[0].id
          return redirect('/success')
        else:
          messages.error(request, "Invalid E-mail or Password")
          return redirect('/')
      else:
        messages.error(request, "Invalid E-mail or Password")
        return redirect('/')
    else:
      messages.error(request, "Invalid E-mail or Password")
      return redirect('/')
  return redirect('/')

def register(request):
  if request.method == "POST":
    if len(User.objects.validation(request.POST)) > 0:
      messages.error(request, User.objects.validation(request.POST))
      return redirect('/')
    else:
      User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=request.POST['password'])
      messages.error(request, "successfully registered")
      return redirect('/')
  return redirect('/')

def success(request):
  request.session['first_name'] = User.objects.get(id=request.session['user_id']).first_name
  return redirect('/travels')

def travels(request):
  if 'user_id' not in request.session:
    messages.error(request, "Please log in")
    return redirect('/')
  travels={
    'myplans':Travelplan.objects.filter(user_id=request.session['user_id']),
    'joinedplans':Travelplan.objects.filter(users=request.session['user_id']),
    'othersplans':Travelplan.objects.all()
  }
  return render(request, 'travels.html', travels)

def add(request):
  if 'user_id' not in request.session:
    messages.error(request, "Please log in")
    return redirect('/')
  return render(request, 'travels_add.html')

def create(request):
  if len(Travelplan.objects.validation(request.POST)) > 0:
    messages.error(request, Travelplan.objects.validation(request.POST))
    return redirect('/travels/add') 
  user = User.objects.get(id=request.session['user_id'])
  Travelplan.objects.create(destination=request.POST['destination'], start=request.POST['start'], end=request.POST['end'], plan=request.POST['description'], user=user)
  return redirect('/travels')

def destination(request, id):
  if 'user_id' not in request.session:
    messages.error(request, "Please log in")
    return redirect('/')
  destination={
    'destination':Travelplan.objects.get(id=id),
    'others':Travelplan.objects.get(id=id).users
  }
  return render(request, 'destination.html', destination)

def join(request, id):
  travel=Travelplan.objects.get(id=id)
  travel.save()
  travel.users.add(User.objects.get(id=request.session['user_id']))
  return redirect('/travels')

def leave(request, user_id, destination_id):
  plan=Travelplan.objects.get(id=destination_id)
  user=User.objects.get(id=user_id)
  plan.users.remove(user)
  return redirect('/destination/'+str(destination_id))

def logout(request):
  request.session.flush()
  return redirect('/')