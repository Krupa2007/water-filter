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
   if request.GET.get('search'):
        quearyset = quearyset.filter(name__icontains = request.GET.get('search')) 

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
    
   # if request.GET.get('search'):
    #    quearyset = quearyset.filter(name__icontains = request.GET.get('search')) 




    context = {'add': quearyset}

    return render(request, "add.html" , context)


def  delete_pet(request, id):
    queryset = Add.objects.get(id = id)
    queryset.delete()
    return redirect('/main')

"""def update(request, id):
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
       return redirect('/main/')

    return render(request, "update.html",context)

"""
from django.shortcuts import render, redirect, get_object_or_404
 # Double-check if your model class name is 'pet' or 'Pet'

def update_data(request, id):
    # 1. Use get_object_or_404 so Django handles missing IDs gracefully instead of crashing
    record = get_object_or_404(Add, id=id)
    
    # 2. When the form is submitted via POST
    if request.method == "POST":
        record.name = request.POST.get('name')
        record.contact = request.POST.get('contact')
        record.email = request.POST.get('email')
        
        # 3. Save the modifications directly back to that existing row
        record.save() 
        
        # 4. Redirect back to your main table display page
        return redirect('/main/') 
        
    # 5. When they first load the page, render update.html with the existing record values
    return render(request, 'update.html', {'record': record})



def analytics_view(request):
    return render(request, "analytics.html")

def model(request):
    return render(request, "model.html")



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
    
def profile(request):
   return render(request,  "profil.html")


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def update_profile(request ,id):
    if request.method == 'POST':
        profile = request.user.profile
        
        profile.description = request.POST.get('description')
        profile.contact = request.POST.get('contact')
        
        # Check if the user clicked "Remove Photo"
        if request.POST.get('clear_image') == 'true':
            # This deletes the image file from media storage and database
            if profile.image:
                profile.image.delete(save=False) 
            profile.image = None
        # Otherwise, check if they uploaded a brand new image
        elif request.FILES.get('profile_pix'):
            profile.image = request.FILES['profile_pix']
            
        profile.save()
        return redirect('profile')
        
    return render(request, 'profile.html')