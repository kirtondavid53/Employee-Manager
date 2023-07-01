from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Employee
from .forms import AddEmployeeForm
from django.db.models import Q
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
import datetime

def index(request):


    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "You successfully logged in.")
            return redirect('index')
        
        else:
            messages.info(request, "There was an error. Please try again.")
            return redirect('index')
        
    
        
    if request.user.is_authenticated:
        current_user = request.user
        records = Employee.objects.filter(user=current_user)
        return render(request, 'index.html', {'records':records})
    
    else:   
        messages.info(request, "Login or register to get started.")
        return render(request, 'index.html')
        
        
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('index')

def record_view(request, pk):
    if request.user.is_authenticated:
     
        current_user = request.user
        record = Employee.objects.get(user=current_user, id=pk)
        
        return render(request, 'record.html', {'record':record}) 
    
    else:
        messages.info(request, "You must be logged in to view this page")
        return redirect('index')
    


@login_required(login_url="index")
def add_employee(request):
    if request.method == "POST":  
          
        current_user = request.user
        form = AddEmployeeForm(request.POST)
        
        if form.is_valid():  
            try:  
                
                item = form.save(commit=False)
                item.user = request.user
                item.save()
                            #model = form.instance
                messages.info(request, "Employee Created") 
                return redirect('index')  
            except:  

                messages.info(request, "There was an error. Please try again") 
                return redirect('add_employee')
    else:  
        form = AddEmployeeForm()  
    return render(request,'create_employee.html',{'form':form})  

def register(request):

    if request.method == 'POST':

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2 :
            if User.objects.filter(email=email).exists():
                messages.warning(request, 'Email is already used')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.warning(request, 'Username has already been used')
                return redirect('register')
            
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                login(request, user)
                return redirect('index')
            
        else:
            messages.warning(request, 'Passwords are not the name')
            return redirect(request, 'register')
        
    else:

        return render(request ,'register.html')
    

@login_required(login_url="index")
def delete_employee(request, pk):
    if request.user.is_authenticated:
     
        current_user = request.user
        record = Employee.objects.get(user=current_user, id=pk)
        record.delete()
        messages.info(request, 'Employee has been deleted')
        return redirect('index')
    
    return redirect('index')


def update_employee(request, pk):
    if request.user.is_authenticated:
        current_user = request.user
        current_record = Employee.objects.get(user=current_user, id=pk)
        form = AddEmployeeForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save() 
            messages.success(request, "Employee has been updated")
            return redirect('index')
        
        return render(request, "update_employee.html", {'form':form})

    else:
        messages.info(request, "You must be logged in to perform this action")
        return redirect('index')
    
@login_required(login_url='index')
def search_records(request):
    if request.method == 'POST':
        search_input = request.POST['search_input']
        current_user = request.user
        current_user_employees = Employee.objects.filter(user=current_user)
        employees = current_user_employees.filter(Q(first_name__contains=search_input) | Q(last_name__contains=search_input) | Q(job_title__contains=search_input)).values()
        return render(request, 'search_records.html', {'search_input':search_input,'employees':employees})

    return render(request, 'search_records.html')


def dashboard_view(request):
    if request.user.is_authenticated:
        curr_user = request.user
        records = Employee.objects.filter(user=curr_user)
        num_records = len(records)
        today = datetime.date.today()
        curr_year = today.year
        curr_month = today.month
        records_this_month = Employee.objects.filter(user=curr_user, date_created__year=curr_year, date_created__month=curr_month)
        sum = records.aggregate(Sum('salary'))
        num_records_this_month = len(records_this_month)

        return render(request, 'dash.html', {"num_records":num_records, "num_records_this_month":num_records_this_month, "curr_user":curr_user, "records_this_month":records_this_month, "sum":sum})

    else:
        messages.info(request, "You must be logged in to view this page")
        return redirect('index')
    
    
    

    

    

        