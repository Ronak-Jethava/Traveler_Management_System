from django.shortcuts import redirect, render
import psycopg2
from decouple import config

# Create your views here.
def home(request):
    return render(request, 'employee_home.html')

def add_traveller(request):
    if request.method == "POST":
        user_name = request.POST.get('user_name')
        first_name = request.POST.get('first_name')
        middle_name = request.POST.get('middle_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        contact = int(request.POST.get('contact'))
        birthdate = request.POST.get('birthdate')
        gender = request.POST.get('gender')
        gender = "Male" if gender=='option1' else "Female"
        password = request.POST.get('password')
        
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
    
        c.execute(f'''
            INSERT INTO "Contact"(user_id, contact_number)
            values ({user_id},{contact})
        ''')
        
        c.execute(f'''
            INSERT INTO "Login"(login_username, login_password, user_id)
            values ('{user_name}', '{password}', {user_id})
        ''')

        c.execute(f'''
            select *
            from "User"
            where user_id = {user_id}
        ''')
        user = c.fetchone()
        conn.commit()
        c.close()
        
        if conn is not None:
            conn.close()
        
        return render(request, 'add_traveller.html', {'user':user,'username':user_name,'password':password,'contact':contact})
    else:
        return render(request, 'add_traveller.html', {'user':None})

def delete_user(request):
    if request.method == "POST":
        user_id = request.POST.get('user_id')

        conn = psycopg2.connect(
            database=config('DB_NAME'), user=config('DB_USER'), password=config('DB_PASSWORD'), host='127.0.0.1', port= '5432'
        )
        c = conn.cursor()
        
        c.execute(f'''
            DELETE
            from "User"
            where user_id = {user_id}
        ''')
        
        conn.commit()
        c.close()
        
        if conn is not None:
            conn.close()

        return render(request, 'delete_user.html', {'deleted':True, 'user_id':user_id})
    
    else:
        return render(request, 'delete_user.html', {'deleted':None})
        