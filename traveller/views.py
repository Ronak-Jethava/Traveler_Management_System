from django.http.response import Http404
from django.shortcuts import render
from dummy.models import User
import psycopg2
from decouple import config

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
            select "Scheduled_on".start_date, (select string_agg("Places".place_name, ', ') from "Places" where "Tour Package".package_id = package_id group by package_id), "Tour Package".vehicle, t1.payment_amount
            from (
                select "Booking".booking_id, (select "Payment".payment_amount from "Payment" where "Payment".booking_id = "Booking".booking_id and "Payment".payment_status='successful'), "Booking".package_detail_id
                from "Booking" 
                where traveller_id = {0}
                ) as t1(booking_id, payment_amount, schedule_id) 
                join "Scheduled_on"
                on t1.schedule_id = "Scheduled_on".schedule_id
                join "Tour Package"
                on "Tour Package".package_id = "Scheduled_on".package_id
       '''.format(user_id))
        travel_history = c.fetchall()
        c.close()

        return render(request, 'get_user_id.html', {'travel_history':travel_history})
    else:
        return render(request, 'get_user_id.html')