from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate , login
from .models import *
from reportlab.pdfgen import canvas
from datetime import datetime

# Create your views here.
def login_page(request):
   if request.method =="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if  not User.objects.filter(username = username).exists():
            messages.error(request, 'Invalid Username')
            return redirect('/login/')
        
        user =authenticate(username = username , password= password)

        if user is None:
            messages.error(request, 'Invalid password')
            return redirect('/login/')
        
        else:
            login( request , user)
            return redirect('/main/')
        


   return render(request,  "login.html")

def register(request):
   if request.method ==  "POST":
         first_name = request.POST.get('first_name')
         last_name = request.POST.get('last_name')
         username = request.POST.get('username')
         password = request.POST.get('password')

         user = User.objects.filter(username = username)
         if user.exists():
             messages.info(request, 'Username already taken')
             return redirect('/register/')
             
       
         user = User.objects.create(
             first_name = first_name,
             last_name = last_name,
             username = username,
         
         )
         user.set_password(password)
         user.save()
         messages.info(request, "Account created sucessfully.")
         return redirect('/register/')



   return render(request,  "register.html")

def forgot(request):
   return render(request,  "forgot.html")

def home(request):
   return render(request,  "home.html")

def main(request):
   quearyset = Add.objects.all()
   context = {'add': quearyset}
   return render(request,  "main.html", context)

def qr(request):
   return render(request,  "qrcode.html")

def water_quality(request):
   return render(request,  "water_quality.html")
 
def dashboard(request):
    return render(request, "dashboard")

def add(request):
    if request.method=="POST":
        data = request.POST
        name = data.get('name')
        email = data.get('email')
        contact = data.get('contact')

        Add.objects.create(
            name= name,
            email = email,
            contact = contact,
        )

    quearyset = Add.objects.all()
    context = {'add': quearyset}

    return render(request, "add.html" , context)


def  delete_pet(request, id):
    queryset = Add.objects.get(id = id)
    queryset.delete()
    return redirect('/main')

def update(request, id):
    queryset = Add.objects.get(id = id)

    if request.method=="POST":
       data = request.POST
       name = data.get('name')
       email = data.get('email')
       contact = data.get('contact')

       queryset.name= name
       queryset.email= email
       queryset.contact= contact


       queryset.save()
       context = {'add': queryset}
       return redirect('/update/')

    return render(request, "update.html",context)


def analytics_view(request):
    return render(request, "analytics.html")



def export_page(request):
    return render(request, "export.html")


def export_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="dashboard_report.pdf"'

    p = canvas.Canvas(response)

    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 800, "Water Filter Monitoring Dashboard")

    p.setFont("Helvetica", 12)
    p.drawString(100, 780, f"Generated on: {datetime.now()}")

    p.drawString(100, 740, "System Status: ONLINE")
    p.drawString(100, 720, "Water Quality: Excellent")
    p.drawString(100, 700, "Filter Health: 92%")

    p.showPage()
    p.save()

    return response
    