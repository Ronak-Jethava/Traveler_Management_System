from django.shortcuts import render
import psycopg2
from decouple import config

# Create your views here.
def home(request):
    return render(request, 'employee_home.html')

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
