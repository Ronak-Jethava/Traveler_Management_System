from django.http.response import HttpResponse
from django.shortcuts import render, HttpResponse
from decouple import config
import psycopg2

# Create your views here.
def home(request):
    return render(request, 'agency_home.html')

def display_packages(request):
    if request.method == "POST":
        agency_id = request.POST.get('agency_id')
        conn = psycopg2.connect(
            database=config('DB_NAME'), user=config('DB_USER'), password=config('DB_PASSWORD'), host='127.0.0.1', port= '5432'
        )
        c = conn.cursor()
        c.execute(f'''
            select *
            from "Travel Agency"
            where agency_id = {agency_id}
        ''')
        travel_agency = c.fetchone()
        
        c.execute(f'''
            select *, (select string_agg("Places".place_name, ',' order by place_name) from "Places" where "Places".package_id="Tour Package".package_id), (select string_agg("Activities".activity_name, ', ' order by activity_name) from "Activities" where "Activities".package_id="Tour Package".package_id)
from "Tour Package"
Where agency_id = {agency_id}
        ''')
        tour_packages = c.fetchall()
        conn.commit()
        c.close()
        
        if conn is not None:
            conn.close()
        print(travel_agency)
        return render(request, 'display_packages.html', {'no_agency':travel_agency is None,'travel_agency':travel_agency,'tour_packages': tour_packages})

    else:
        return render(request, 'display_packages.html', {'no_agency':False,'travel_agency':None,'tour_packages':None})
