from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
# Create your views here.
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'index/index.html')


def about(request):
    return render(request, 'index/about.html')


def contact(request):
    return render(request, 'index/contact.html')


def vehicle_list(request):
    data = {
        'types': VehicleType.objects.all(),
    }
    if request.GET.get('type'):
        data['types'] = VehicleType.objects.filter(id__in=request.GET.getlist('type'))

    return render(request, 'vehicle/list.html', data)


def vehicle_detail(request, pk):
    data = {
        'vehicle': Vehicle.objects.get(id=pk),
    }
    return render(request, 'vehicle/detail.html', data)

@login_required(login_url='/login')
def booking(request, pk):
    data = {
        'vehicle': Vehicle.objects.get(id=pk),
        'today': datetime.now().strftime('%Y-%m-%d'),
        }
    if request.method == 'POST':
        try:
            distance_val = int(request.POST.get('distance_value'))
            vehicle = Vehicle.objects.get(id=pk)
            if(request.POST.get('type') == 'oneway'):
                days = ceil(distance_val/(500*1000))
                total = (vehicle.per_km * (distance_val)/1000) + (vehicle.min_fare*days)
                #check if any day trip is booked on the same day
                if Trip.objects.filter(vehicle=Vehicle.objects.get(id=pk), start_date=request.POST.get('start_date').split(' to ')[0]).exists():
                    raise Exception('A trip is already booked on the same day')
                trip = Trip.objects.create(
                    vehicle=Vehicle.objects.get(id=pk),
                    type='One Way',
                    start_date=request.POST.get('start_date').split(' to ')[0],
                    start_time=request.POST.get('start_time'),
                    pickup = request.POST.get('pickup'),
                    destination = request.POST.get('destination'),
                    distance = f"{distance_val/1000} km",
                    user=request.user,
                    total_cost = total,
                )
            elif (request.POST.get('type') == 'roundtrip'):
                total = Vehicle.objects.get(id=pk).per_km * (distance_val)/1000 * 2
                if Trip.objects.filter(vehicle=Vehicle.objects.get(id=pk), start_date=request.POST.get('start_date').split(' to ')[0]).exists():
                    raise Exception('A trip is already booked on the same day')
                trip = Trip.objects.create(
                    vehicle=Vehicle.objects.get(id=pk),
                    type='Round Trip',
                    start_date=request.POST.get('start_date').split(' to ')[0],
                    start_time=request.POST.get('start_time'),
                    pickup=request.POST.get('pickup'),
                    destination=request.POST.get('destination'),
                    distance = f"{int(request.POST.get('distance_value'))/1000} km",
                    user=request.user,
                    total_cost=total,
                )
            else:
                dates = request.POST.get('start_date').split(' to ')
                start_date = datetime.strptime(dates[0], '%Y-%m-%d').date()
                end_date = datetime.strptime(dates[1], '%Y-%m-%d').date()
                days = (end_date - start_date).days + 1
                total = (Vehicle.objects.get(id=pk).per_day * days) + 700
                #check if any oneway or roundtrip is booked in between the dates and any day trip overlaps with the dates
                if Trip.objects.filter(vehicle=Vehicle.objects.get(id=pk), start_date__gte=start_date, start_date__lte=end_date).exists():
                    raise Exception('A trip is already booked in between the dates') 

                trip = Trip.objects.create(
                    vehicle=Vehicle.objects.get(id=pk),
                    type='Day Trip',
                    start_date=start_date,
                    start_time=request.POST.get('start_time'),
                    end_date=end_date,
                    pickup=request.POST.get('pickup'),
                    destination=request.POST.get('destination'),
                    days=days,
                    user=request.user,
                    total_cost=total,
                )
            return redirect('trip_detail', pk=trip.id)
        except Exception as e:
            data['error'] = str(e)
    return render(request, 'vehicle/booking.html', data)


def booking_status(request, pk):
    return render(request, 'vehicle/status.html')



"""
User and profile
"""



def login(request):
    data = {}
    if request.method == 'POST':
        try:
            email = request.POST.get('email')
            password = request.POST.get('password')
            try:
                username = User.objects.get(email=email).username
            except:
                raise Exception('User does not exist')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))
                return redirect('index')
            raise Exception('Invalid credentials')
        except Exception as e:
            data['error'] = str(e)
        
    return render(request, 'auth/login.html', data)


def register(request):
    if request.method == 'POST':
        try:
            email = request.POST.get('email')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm-password')
            if password != confirm_password:
                raise Exception('Password does not match')
            username = email
            user = User.objects.create_user(username=username, email=email, password=password)
            if request.POST.get('name'):
                #convert name into first and last_name
                name = request.POST.get('name').split(' ')
                user.first_name = name[0]
                user.last_name = ' '.join(name[1:])
            profile = Profile.objects.create(user=user, phone=request.POST.get('phone'), email=email)
            user.save()
            profile.save()
            return redirect('login')
        except Exception as e:
            data = {
                'error': str(e)
            }
            return render(request, 'auth/register.html', data)
    return render(request, 'auth/register.html')

@login_required(login_url='/login')
def profile(request):
    if request.method == 'POST':
        user = request.user
        name = request.POST.get('name').split(' ')
        user.first_name = name[0]
        user.last_name = ' '.join(name[1:])
        user.profile.email = request.POST.get('email')
        user.profile.phone = request.POST.get('phone')
        user.save()
        user.profile.save()
        return redirect ('profile')
    return render(request, 'user/profile.html')


def logout(request):
    if request.method == 'POST':
        auth_logout(request)
        return redirect('index')
    return render(request, 'user/logout.html')


@login_required(login_url='/login')
def trip_list(request):
    data={
        'trips': Trip.objects.filter(user=request.user)
    }
    return render(request, 'user/trip_list.html', data)


@login_required(login_url='/login')
def trip_detail(request, pk):
    data={}
    try:
        data['trip'] = Trip.objects.get(pk=pk)
        if data['trip'].user != request.user:
            raise Exception
    except:
        data['error']  = "Trip not found"
    return render(request, 'user/trip_detail.html', data)


@login_required(login_url='/login')
def trip_cancel(request, pk):
    data={}
    try:
        trip = Trip.objects.get(pk=pk)
        if trip.user != request.user:
            raise Exception
        data['trip'] = trip
        can_cancel = True
        reason = ""

        now = datetime.now()
        trip_datetime = datetime.combine(trip.start_date, trip.start_time)
        if now + timedelta(hours=2) >= trip_datetime:
            can_cancel =  False
            reason = "Less than 2 hours left."
        if trip.status in ['Completed', 'Started', 'Cancelled']:
            can_cancel = False
            reason = "trip is "+trip.status

        data['can_cancel'] = can_cancel
        data['reason'] = reason       
        if request.method=='POST':
            trip.status = 'Cancelled'
            trip.save()
            return redirect('trip_cancel', pk=pk)
    except:
        data['error']  = "Trip not found"
    return render(request, 'user/trip_cancel.html', data)



def api_trip_list(request):
    try:
        vehicle = Vehicle.objects.get(id=request.GET.get('vehicle'))
        pk = vehicle.id
    except:
        return JsonResponse({'error': 'Vehicle not found', 'status':404})
    try:
        trips = []
        for trip in Trip.objects.filter(vehicle=Vehicle.objects.get(id=int(request.GET.get('vehicle')))).filter(Q(end_date__gte=datetime.now().date()) | Q(start_date__gte=datetime.now().date())):
            if trip.status in ['Pending', 'Started', 'Confirmed']:
                trips.append({
                    'start_date': trip.start_date - timedelta(days=1),
                    'end_date': trip.end_date if trip.end_date else trip.start_date,
                })
        return JsonResponse({'trips': trips, 'status':200})
    except Exception as e:
        return JsonResponse({'error': str(e), 'status':500})
    
    