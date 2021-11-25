from django.http.response import Http404
from django.shortcuts import get_list_or_404, render
import psycopg2
from decouple import config
from datetime import datetime

# Create your views here.
def home(request):
    return render(request, 'traveller_home.html')

def travel_history(request):
    if request.method == "POST":
        user_id = int(request.POST.get('user_id'))
        conn = psycopg2.connect(
            database=config('DB_NAME'), user=config('DB_USER'), password=config('DB_PASSWORD'), host='127.0.0.1', port= '5432'
        )
        c = conn.cursor()
        c.execute('''
            select "Scheduled_on".start_date, (select string_agg("Places".place_name, ', ') from "Places" where "Tour Package".package_id = package_id group by package_id), "Tour Package".vehicle, "Tour Package".duration, t1.no_of_seats, t1.payment_amount, t1.payment_date, t1.payment_time, t1.payment_mode
            from (
                select "Booking".booking_id, "Payment".payment_amount, "Payment".payment_date, "Payment"."Payment_time", "Payment".payment_mode, "Booking".package_detail_id, "Booking".no_of_seats
                from "Booking" join "Payment"
				on "Payment".booking_id = "Booking".booking_id and "Payment".payment_status = 'successful'
                where traveller_id = {0}
                ) as t1(booking_id, payment_amount, payment_date, payment_time, payment_mode, schedule_id, no_of_seats) 
                join "Scheduled_on"
                on t1.schedule_id = "Scheduled_on".schedule_id
                join "Tour Package"
                on "Tour Package".package_id = "Scheduled_on".package_id
                where "Scheduled_on".start_date < current_date or ("Scheduled_on".start_date = current_date and start_time < current_time)
       '''.format(user_id))
        travel_history = c.fetchall()
        c.close()
        if conn is not None:
            conn.close()
        
        return render(request, 'travel_history.html', {'traveller_id':user_id, 'travel_history':travel_history})
    else:
        return render(request, 'travel_history.html')


def upcoming_tours(request):
    if request.method == "POST":
        user_id = int(request.POST.get('user_id'))
        conn = psycopg2.connect(
            database=config('DB_NAME'), user=config('DB_USER'), password=config('DB_PASSWORD'), host='127.0.0.1', port= '5432'
        )
        c = conn.cursor()
        c.execute('''
            select "Scheduled_on".start_date, (select string_agg("Places".place_name, ', ') from "Places" where "Tour Package".package_id = package_id group by package_id), "Tour Package".vehicle, "Tour Package".duration, t1.no_of_seats, t1.payment_amount, t1.payment_date, t1.payment_time, t1.payment_mode, "Scheduled_on".start_time
            from (
                select "Booking".booking_id, "Payment".payment_amount, "Payment".payment_date, "Payment"."Payment_time", "Payment".payment_mode, "Booking".package_detail_id, "Booking".no_of_seats
                from "Booking" join "Payment"
				on "Payment".booking_id = "Booking".booking_id and "Payment".payment_status = 'successful'
                where traveller_id = {0}
                ) as t1(booking_id, payment_amount, payment_date, payment_time, payment_mode, schedule_id, no_of_seats) 
                join "Scheduled_on"
                on t1.schedule_id = "Scheduled_on".schedule_id
                join "Tour Package"
                on "Tour Package".package_id = "Scheduled_on".package_id
                where "Scheduled_on".start_date > current_date or ("Scheduled_on".start_date = current_date and start_time >= current_time)
       '''.format(user_id))
        upcoming_tours = c.fetchall()
        c.close()
        if conn is not None:
            conn.close()
        
        return render(request, 'upcoming_tours.html', {'traveller_id':user_id, 'upcoming_tours':upcoming_tours})
    else:
        return render(request, 'upcoming_tours.html')


def explore_tour_packages(request):
    conn = psycopg2.connect(
        database=config('DB_NAME'), user=config('DB_USER'), password=config('DB_PASSWORD'), host='127.0.0.1', port= '5432'
    )
    c = conn.cursor()
    c.execute('''
        select "Tour Package".*, "Scheduled_on".*, (select string_agg("Places".place_name, ', ' order by place_name) from "Places" where "Places".package_id="Tour Package".package_id), (select string_agg("Activities".activity_name, ', ' order by activity_name) from "Activities" where "Activities".package_id="Tour Package".package_id), (select customer_care_number from "Travel Agency" where "Tour Package".agency_id = "Travel Agency".agency_id)
        from (
            "Tour Package" join "Scheduled_on"
            on "Tour Package".package_id = "Scheduled_on".package_id
        )
        where start_date > current_date or start_date = current_date and start_time > current_time
    ''')
    tours = c.fetchall()
    
    if request.method == "POST":
        vehicles = request.POST.getlist('vehicle')
        if vehicles:
            tours = list(filter(lambda x:x[3] in vehicles, tours))

        s_date = request.POST.get('s_date')
        e_date = request.POST.get('e_date')

        if s_date:
            [y,m,d] = list(map(int,s_date.split('-')))
            tours = list(filter(lambda x:x[11] > datetime(y,m,d).date() or x[11] == datetime(y,m,d).date() and x[12] >= datetime.now(), tours))

        if e_date:
            [y,m,d] = list(map(int,e_date.split('-')))
            tours = list(filter(lambda x:x[11] <= datetime(y,m,d).date(), tours))

        e_amnt = request.POST.get('e_amnt')

        if e_amnt:
            tours = list(filter(lambda x:x[5] <= int(e_amnt), tours))

        places = request.POST.get('places')
        places = [item.lower() for item in list(places.split(',')) if item]
        if places:
            tours = list(filter(lambda x:(x[15] is not None and any(place in places for place in [s.lower() for s in x[15].split(', ')])), tours))

        activities = request.POST.get('activities')
        activities = [item.lower() for item in list(activities.split(',')) if item]
        if activities:
            tours = list(filter(lambda x:(x[16] is not None and any(activity in activities for activity in [s.lower() for s in x[16].split(', ')])), tours))

    c.close()
    if conn is not None:
        conn.close()
    
    return render(request, 'explore_tours.html', {'tours':tours})
