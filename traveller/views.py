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
        if conn is not None:
            conn.close()
        
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
        if conn is not None:
            conn.close()
        
        return render(request, 'upcoming_tours.html', {'upcoming_tours':upcoming_tours})
    else:
        return render(request, 'upcoming_tours.html')


def add_traveller(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        middle_name = request.POST.get('middle_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        birthdate = request.POST.get('birth_date')
        birthdate = str(birthdate)
        gender = request.POST.get('gender')
        gender = "MALE" if gender == 0 else "FEMALE"
        vaccinated = request.POST.get('vaccinated')

        conn = psycopg2.connect(
            database=config('DB_NAME'), user=config('DB_USER'), password=config('DB_PASSWORD'), host='127.0.0.1', port= '5432'
        )
        c = conn.cursor()
        c.execute('''
            select max(user_id)+1
            from "User"
        ''')
        user_id = c.fetchone()[0]
        
        c.execute(f'''
            INSERT INTO public."User"(
	            user_id, first_name, middle_name, last_name, user_email, birthdate, gender, signup_since)
	                VALUES ({user_id}, '{first_name}', '{middle_name}', '{last_name}', '{email}', '{birthdate}'::date, '{gender}', current_date);
        ''')

        c.execute(f'''
        INSERT INTO public."Traveller"(
            traveller_id, is_fully_vaccinated, vacctination_certificate_oid)
            VALUES ({user_id}, false, null);
    ''')
        conn.commit()
        c.close()
        
        if conn is not None:
            conn.close()
        

        print(first_name, middle_name, last_name, email, birthdate, gender)
        return render(request, 'add_traveller.html')
    else:
        return render(request, 'add_traveller.html')
