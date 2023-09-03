from django.shortcuts import render, redirect
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from . models import Event, Venue
from . forms import VenueForm, EventForm
from django.http import HttpResponseRedirect, HttpResponse
from django.http import FileResponse
import io
import csv
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
# Create your views here.


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
    event.delete()
    return redirect('list-events')    

def update_event(request,event_id):
    event = Event.objects.get(pk=event_id)
    form = EventForm(request.POST or None, instance=event)

    if form.is_valid():
        form.save()
        return redirect('list-events')
    return render(request, 'events/update_event.html', { 'event' : event, 'form' : form})



def add_event(request):
    submitted = False
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_event?submitted=True')
    
    else:
        form =  EventForm
        if 'submitted' in request.GET :
            submitted = True 

            
    return render(request, 'events/add_event.html',{'form' : form, 'submitted' : submitted})


def update_venue(request,venue_id):
    venue = Venue.objects.get(pk=venue_id)
    form = VenueForm(request.POST or None, instance=venue)

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
    return render(request, 'events/show_venue.html', { 'venue' : venue})

def list_venues(request):
    venue_list = Venue.objects.all()
    return render(request, 'events/venues.html', {'venue_list' : venue_list} )


def add_venue(request):
    submitted = False
    if request.method == "POST":
        form = VenueForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_venue?submitted=True')
    
    else:
        form =  VenueForm
        if 'submitted' in request.GET :
            submitted = True 

            
    return render(request, 'events/add_venue.html',{'form' : form, 'submitted' : submitted})


def all_events(request):
    event_list = Event.objects.all().order_by('event_date', 'venue')
    return render(request, 'events/event_list.html', {'event_list' : event_list})


def home(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
    name = 'Aditya'
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

    return render(request, "events/home.html",{
        'name': name,
        'year': year,
        'month': month,
        'month_number': month_number,
        "cal" : cal,
        "current_year" : current_year,
        "time" : time,
    })
