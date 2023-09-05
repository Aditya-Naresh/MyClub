from django.shortcuts import render, redirect
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from . models import Event, Venue
from django.contrib.auth.models import User
from . forms import VenueForm, EventFormAdmin, UserEventForm
from django.http import HttpResponseRedirect, HttpResponse
from django.http import FileResponse
import io
import csv
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

from django.contrib import messages

from django.core.paginator import Paginator
# Create your views here.



# Admin Event Approval
def admin_approval(request):
    event_list =Event.objects.all().order_by('-event_date')
    if request.user.is_superuser:
        if request.method == "POST":
            id_list = request.POST.getlist('boxes')
        #  Uncheck everything
            event_list.update(approved=False)
        #    Update the database
            for x in id_list:
                Event.objects.filter(pk=int(x)).update(approved = True)
            messages.success(request,'Approval has been Updated')
            return redirect('list-events')
        else:    
            return render(request, 'events/admin_approval.html',{"event_list" : event_list})

    else:
        messages.success(request,'You are not authorised to use this')
        return redirect('home')
    return render(request, 'events/admin_approval.html')


# Search Events
def search_events(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        events = Event.objects.filter(name__contains = searched)
        return render(request, 'events/search_events.html',{'searched' : searched,  'events':events})
    else:
        return render(request, 'events/search_events.html',{})



# My Events Page
def my_events(request):
    if request.user.is_authenticated:
        me = request.user.id
        events = Event.objects.filter(attendees = me)
        return render(request, 'events/my_events.html', {'events' : events, 'me' : me })
    else:
        messages.success(request, "You are not authorised to view this page")
        return redirect('home')

# Generate PDF file
def venue_pdf(request):
    # Create a byte stream buffer
    buf = io.BytesIO()
    # Create a canvas
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    #  Create a text object
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)

    # Designate Models
    venues = Venue.objects.all()

    lines = []

    for venue in venues:
        lines.append(venue.name)
        lines.append(venue.address)
        lines.append(venue.zip_code)
        lines.append(venue.phone)
        lines.append(venue.website)
        lines.append(venue.email_address)
        lines.append("--------------------------------")

    for line in lines:
        textob.textLine(line)

    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)


    return FileResponse(buf, as_attachment=True, filename='Venue.pdf')

#Generate List as CSV file
def venue_csv(request):
    response = HttpResponse(content_type = 'text/csv')
    response['Content-Disposition'] = 'attachment; filename = venues.csv'

    # Create a CSV writer
    writer = csv.writer(response)

    #Designate the models
    venues = Venue.objects.all()


    # Add columns to CSV
    writer.writerow(['Venue Name', 'Address', 'Zip Code', 'Phone', 'Website', "Email"])

  
    #Loop through
    for venue in venues:
        writer.writerow([venue.name,venue.address ,venue.zip_code, venue.phone, venue.website, venue.email_address])

    return response
    

# Generate Venue List as a txt file
def venue_text(request):
    response = HttpResponse(content_type = 'text/plain')
    response['Content-Disposition'] = 'attachment; filename = venues.txt'

    #Designate the models
    venues = Venue.objects.all()

    lines = []
    #Loop through
    for venue in venues:
        lines.append(f'Venue: {venue.name} \n Address : {venue.address} \n Zip Code : {venue.zip_code} \n Phone : {venue.phone} \n Web : {venue.website} \n Email : {venue.email_address} \n\n\n\n')

    # write to text
    response.writelines(lines)
    

    return response

def delete_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue.delete()
    return redirect('list-venues')  




def delete_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.user == event.manager:
        event.delete()
        messages.success(request, f"{event.name} deleted")
        return redirect('list-events')
    else:
        messages.success(request, "You're not authorised to Delete this event")
        return redirect('list-events')    

def update_event(request,event_id):
    event = Event.objects.get(pk=event_id)
    if request.user.is_superuser:
        form = EventFormAdmin(request.POST or None, instance=event)
    else:
        form = UserEventForm(request.POST or None, instance=event)
    if form.is_valid():
        form.save()
        return redirect('list-events')
    return render(request, 'events/update_event.html', { 'event' : event, 'form' : form})



def add_event(request):
    submitted = False
    if request.method == "POST":
        if request.user.is_superuser:
            form = EventFormAdmin(request.POST)
        else:
            form = UserEventForm(request.POST)

        if form.is_valid():
            if not request.user.is_superuser:
                event = form.save(commit=False)
                event.manager = request.user
                event.save()
            else:
                form.save()
            return HttpResponseRedirect('/add_event?submitted=True')
    
    else:
        if request.user.is_superuser:
            form = EventFormAdmin()
        else:
            form = UserEventForm()

        if 'submitted' in request.GET:
            submitted = True 

    return render(request, 'events/add_event.html', {'form': form, 'submitted': submitted})



def update_venue(request,venue_id):
    venue = Venue.objects.get(pk=venue_id)
    form = VenueForm(request.POST or None, request.FILES or None,  instance=venue)

    if form.is_valid():
        form.save()
        return redirect('list-venues')
    return render(request, 'events/update_venue.html', { 'venue' : venue, 'form' : form})


def search_venues(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        venues = Venue.objects.filter(name__contains = searched)
        return render(request, 'events/search_venues.html',{'searched':searched, 'venues':venues})
    else:
        return render(request, 'events/search_venues.html',{})



def show_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue_owner = User.objects.get(pk=venue.owner)
    return render(request, 'events/show_venue.html', { 'venue' : venue, 'venue_owner': venue_owner})



def list_venues(request):
    venue_list = Venue.objects.all()

    # Setup for pagination
    p = Paginator(Venue.objects.all(), 1)
    page = request.GET.get('page')
    venues = p.get_page(page)
    nums = "a" * venues.paginator.num_pages #Not Sure if it's standard method
    return render(request, 'events/venues.html', {'venue_list' : venue_list, 'venues' : venues, 'nums':nums} )


def add_venue(request):
    submitted = False
    if request.method == "POST":
        form = VenueForm(request.POST, request.FILES)
        if form.is_valid():
            venue = form.save(commit=False)
            venue.owner = request.user.id
            venue.save()
            # form.save()
            return HttpResponseRedirect('/add_venue?submitted=True')
    
    else:
        form =  VenueForm
        if 'submitted' in request.GET :
            submitted = True 

            
    return render(request, 'events/add_venue.html',{'form' : form, 'submitted' : submitted})


def all_events(request):
    event_list = Event.objects.all().order_by('-event_date', 'venue')
    return render(request, 'events/event_list.html', {'event_list' : event_list})


def home(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
    
    
    month = month.title()

    # Convert Month name  into month number
    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)

    # Create Calendar
    cal = HTMLCalendar().formatmonth(year, month_number)

    # Current year
    now = datetime.now()
    current_year = now.year

    # Current time
    time = now.strftime('%I: %M: %p')

    # Query Event Model
    event_list = Event.objects.filter(
        event_date__year = year, event_date__month = month_number
    )
    return render(request, "events/home.html",{
        'year': year,
        'month': month,
        'month_number': month_number,
        "cal" : cal,
        "current_year" : current_year,
        "time" : time,
        "event_list" : event_list,
    })
