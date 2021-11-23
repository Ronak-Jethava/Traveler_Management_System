from django.http.response import Http404
from django.shortcuts import render
from dummy.models import User
import psycopg2
from decouple import config
import datetime

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

        return render(request, 'travel_history.html', {'travel_history':travel_history})
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

        return render(request, 'upcoming_tours.html', {'upcoming_tours':upcoming_tours})
    else:
        return render(request, 'upcoming_tours.html')

