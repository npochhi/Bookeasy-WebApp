from django.shortcuts import get_object_or_404,render, redirect, render
from .models import *
import json
from django.views.decorators import csrf
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib import messages
from django.core.exceptions import *
from django.utils.dateparse import parse_datetime
import datetime
from django.views.decorators.cache import never_cache

@never_cache
# Create your views here.
def home(request):
    if 'id' in request.session.keys():
        if request.session['type'] == 'student':
            studentname = Student.objects.get(email = request.session['id'])
            context = {
                'name': studentname.name
            }
            return render(request, 'studenthome.html', context)
        else:
            employeename = Employee.objects.get(email = request.session['id'])
            context = {
                'name': employeename.name
            }
            return render(request, 'employeehome.html', context)
    else:
        return render(request, 'login.html')

@never_cache
def login(request):
    if request.method == 'POST':
        email = request.POST.get('emailid')
        print(email)
        password = request.POST.get('password')
        try: 
            Student.objects.get(email = email)
            student = UserProfile.objects.get(email = email)
            if student.check_pass(password):
                request.session['id'] = email
                request.session['type'] = 'student'
            return redirect('/')
        except: 
            try: 
                Employee.objects.get(email = email)
                employee = UserProfile.objects.get(email = email)
                if employee.check_pass(password):
                    request.session['id'] = email
                    request.session['type'] = 'employee'
                return redirect('/')
            except:
                messages.error(request, 'Username and/or Password is/are incorrect!')
                return redirect('/login')
    else:
        return render(request, 'login.html')

@never_cache
def signup(request):
    if request.method == 'POST':
        email = request.POST.get('emailid')
        print(email)
        pass1 = request.POST.get('pass1')
        print(pass1)
        pass2 = request.POST.get('pass2')
        print(pass2)
        try:
            studentobj = Student.objects.get(email = email)
            try:
                UserProfile.objects.get(email = email)
                messages.error(request, 'An account with this email id already exists in the database!')
                return redirect('/signup')
            except:
                if pass1 == pass2:
                    user = UserProfile(email = email, password = pass1, name = studentobj.name, institute_id = studentobj.ID)
                    user.save()
                    print("here")
                    messages.error(request, 'User successfully created!')
                    return redirect('/signup')
                else:
                    messages.error(request, 'Passwords do not match!')
                    return redirect('/signup')
        except:
            try:
                employeeobj = Employee.objects.get(email = email)
                try:
                    UserProfile.objects.get(email = email)
                    messages.error(request, 'An account with this email id already exists in the database!')
                    return redirect('/signup')
                except:
                    if pass1 == pass2:
                        user = UserProfile(email = email, password = pass1, name = employeeobj.name, institute_id = employeeobj.ID)
                        user.save()
                        messages.error(request, 'User successfully created!')
                        return redirect('/signup')
                    else:
                        messages.error(request, 'Passwords do not match!')
                        return redirect('/signup')
            except:
                messages.error(request, 'No such email id exists in our database!')
                return redirect('/signup/')
    else:
        return render(request, 'signup.html')

@never_cache
def make_booking(request):
    try:
        email = request.session['id']
        guesthouse = request.POST.get('guesthouse')
        category = request.POST.get('category')
        purpose = request.POST.get('purpose')
        doarrival = request.POST.get('doa') 
        dodeparture = request.POST.get('dod')
        dobooking = datetime.datetime.now()
        room_type = request.POST.get('room_type')
        no_rooms = request.POST.get('no_rooms')
        guests = []

        no_occ = 0
        list_disapprovals = list(DisapprovedBookings.objects.all())
        list_bookings_till_now = list(Bookings.objects.filter(dodeparture__gte = datetime.datetime.now(), category = category))
        for booking in list_bookings_till_now:
            count = 0
            for disappbooking in list_disapprovals:
                if disappbooking.booking_id.id == booking.id:
                    count += 1
            if count == 0:
                no_occ += 1       

        guesthouse_obj = GuestHouse.objects.get(name = guesthouse)
        guesthouse_max_occ = Rooms.objects.get(gID = guesthouse_obj, room_type = category).no_available

        if no_occ == guesthouse_max_occ:
            messages.error(request, 'Guesthouse full! Either select other category or change the GuestHouse')
            return redirect('/signup/') 

        for i in range(int(request.POST.get('no_guests'))):
            guest = Guest(email = request.POST.get('guest' + str(i)), name = request.POST.get('name' + str(i)))
            guests += [guest]
            guest.save()
        booking = Bookings(
            category = category, 
            purpose = purpose, 
            doarrival = parse_datetime(doarrival),
            dodeparture = parse_datetime(dodeparture),
            dobooking = parse_datetime(dobooking),
            room_type = room_type
        )
        for guest in guests:
            booking.guests.add(guest)
        booking.booker.add(UserProfile.objects.get(email = email))
        booking.save()
        return redirect('/')
    except:
        return redirect('/')

@never_cache
def approve(request):
    booking_id = request.POST['id']
    booking = Bookings.objects.get(id = booking_id)
    app_booking = ApprovedBookings(booking_id = booking)
    app_booking.save()
    return redirect('/bookingstoapprove')

@never_cache
def disapprove(request):
    booking_id = request.POST['id']
    reason = request.POST['reason']
    booking = Bookings.objects.get(id = booking_id)
    disapp_booking = DisapprovedBookings(booking_id = booking, reason = reason)
    disapp_booking.save()
    return redirect('/bookingstoapprove')

def logout(request):
    del request.session['id']
    del request.session['type']
    request.session.modified = True
    return render(request, 'logout.html')

@never_cache
def bookings_for_approval(request):
    d = []
    try:
        print("Hello1")
        employee = Employee.objects.get(email = request.session['id'])
        approval_entity = list(ApprovalEntity.objects.all())
        bookings = list(Bookings.objects.all())
        for approval_e in approval_entity:
            print(approval_e.approval_ID)
            if approval_e.approval_ID.email == employee.email:
                print(str(approval_e.approval_ID) + "Debug")
                for book in bookings:
                    print(book.doarrival.date)
                    print(datetime.date.today())
                    if approval_e.user_ID == book.booker and book.doarrival.date() > datetime.date.today():
                        try:
                            temp = ApprovedBookings.objects.get(booking_id = book)
                        except:
                            try:
                                temp = DisapprovedBookings.objects.get(booking_id = book)
                            except:
                                #print(book)
                                d.append(book)
        context = {
            'list' : d
        }
        return render(request, 'bookings_to_approve.html', context)
    except:
        context = {
            'list' : d
        }
        return render(request, 'bookings_to_approve.html', context)