from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from tecuroapp.forms import UserForm, DoctorForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

# Create your views here.
def home(request):
    return redirect(doctor_home)

@login_required(login_url='/doctor/sign-in/')
def doctor_home(request):
    return render(request, 'doctor/home.html', {})

@login_required(login_url='/doctor/sign-in/')
def doctor_account(request):
    return render(request, 'doctor/account.html', {})

@login_required(login_url='/doctor/sign-in/')
def doctor_procedure(request):
    return render(request, 'doctor/procedure.html', {})

@login_required(login_url='/doctor/sign-in/')
def doctor_appointment(request):
    return render(request, 'doctor/appointment.html', {})

@login_required(login_url='/doctor/sign-in/')
def doctor_report(request):
    return render(request, 'doctor/report.html', {})

def doctor_sign_up(request):
    user_form = UserForm()
    doctor_form = DoctorForm()

    if request.method == "POST":
        user_form = UserForm(request.POST)
        doctor_form = DoctorForm(request.POST, request.FILES)

        if user_form.is_valid() and doctor_form.is_valid():
            new_user = User.objects.create_user(**user_form.cleaned_data)
            new_doctor = doctor_form.save(commit=False)
            new_doctor.user = new_user
            new_doctor.save()

            login(request, authenticate(
                username = user_form.cleaned_data["username"],
                password = user_form.cleaned_data["password"]
            ))

            return redirect(doctor_home)

    return render(request, "doctor/sign_up.html", {
        "user_form": user_form,
        "doctor_form": doctor_form
    })
