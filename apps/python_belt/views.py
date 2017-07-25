from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Trip

def flashErrors(request, errors):
    for error in errors:
        messages.error(request, error)

def currentUser(request):
    id = request.session['user_id']

    return User.objects.get(id=id)

def index(request):
    return render(request, 'python_belt/index.html')

def travels(request):
    if 'user_id' in request.session:

        current_user = currentUser(request)

        trips = Trip.objects.all()

        context = {
            'current_user': current_user,
            'trips': trips,
        }

        return render(request, 'python_belt/travels.html', context)

    return redirect('/')

def logout(request):
    if 'user_id' in request.session:
        request.session.pop('user_id')
        return redirect('/')

def login(request):
    if request.method == 'POST':

        errors = User.objects.validateLogin(request.POST)

        if not errors:
            user = User.objects.filter(username=request.POST['username']).first()

            if user:
                if str(request.POST['password']) == str(user.password):
                    request.session['user_id'] = user.id

                    return redirect('/travels')


            errors.append("Invalid password")
        flashErrors(request, errors)

    return redirect('/')


def register(request):
    if request.method == 'POST':
        errors = User.objects.validateRegistration(request.POST)

        if not errors:

            user = User.objects.create(

            name=request.POST['name'],
            username=request.POST['username'],
            password=request.POST['password'],

            )

            request.session['user_id'] = user.id


            return redirect('/travels')

        else:
            for error in errors:
                messages.error(request, error)

            return redirect('/')

def addTrip(request):
    if request.method == 'POST':
        errors = Trip.objects.validateTrip(request.POST)

        current_user = currentUser(request)

        if not errors:
            trip = Trip.objects.addTrip(request.POST, current_user)

            request.session['trip_id'] = trip.id

            return redirect('/travels')

        else:
            flashErrors(request, errors)


    return redirect('/add')

def add(request):
    return render(request, 'python_belt/add.html')

def destination(request, id):
    trip = Trip.objects.get(id=id)

    travelers = trip.travelers.all()

    context = {
        'trip': trip,
        'travelers':travelers
        }

    return render(request, 'python_belt/destination.html', context)

def join(request, id):
    current_user = currentUser(request)

    trip = Trip.objects.get(id=id)

    trip.travelers.add(current_user)

    return redirect('/travels')
