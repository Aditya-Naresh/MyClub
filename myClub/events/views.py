from django.shortcuts import render
import calendar
from calendar import HTMLCalendar
from datetime import datetime
# Create your views here.

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
