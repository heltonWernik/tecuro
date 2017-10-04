from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from tecuroapp.forms import UserForm, DoctorForm, UserFormForEdit, ProcedureForm
from django.contrib.auth import authenticate, login

from django.contrib.auth.models import User
from tecuroapp.models import Procedure, Appointment

# Create your views here.
def home(request):
    return redirect(doctor_home)

@login_required(login_url='/doctor/sign-in/')
def doctor_home(request):
    return redirect(doctor_appointment)

@login_required(login_url='/doctor/sign-in/')
def doctor_account(request):
    user_form = UserFormForEdit(instance = request.user)
    doctor_form = DoctorForm(instance = request.user.doctor)

    if request.method == "POST":
        user_form = UserFormForEdit(request.POST, instance = request.user)
        doctor_form = DoctorForm(request.POST, request.FILES, instance = request.user.doctor)

        if user_form.is_valid() and doctor_form.is_valid():
            user_form.save()
            doctor_form.save()

    return render(request, 'doctor/account.html', {
        "user_form": user_form,
        "doctor_form": doctor_form
        })

@login_required(login_url='/doctor/sign-in/')
def doctor_procedure(request):
    procedures = Procedure.objects.filter(doctor = request.user.doctor).order_by("-id")
    return render(request, 'doctor/procedure.html', {"procedures": procedures})

@login_required(login_url='/doctor/sign-in/')
def doctor_add_procedure(request):
    form = ProcedureForm()

    if request.method == "POST":
        form = ProcedureForm(request.POST, request.FILES)

        if form.is_valid():
            procedure = form.save(commit=False)
            procedure.doctor = request.user.doctor
            procedure.save()
            return redirect(doctor_procedure)

    return render(request, 'doctor/add_procedure.html', {
        "form": form
    })

@login_required(login_url='/doctor/sign-in/')
def doctor_edit_procedure(request, procedure_id):
    form = ProcedureForm(instance = Procedure.objects.get(id = procedure_id))
    form.fields['image'].required = False

    if request.method == "POST":
        form = ProcedureForm(request.POST, request.FILES, instance = Procedure.objects.get(id = procedure_id))

        if form.is_valid():
            form.save()
            return redirect(doctor_procedure)

    return render(request, 'doctor/edit_procedure.html', {
        "form": form
    })

@login_required(login_url='/doctor/sign-in/')
def doctor_appointment(request):
    if request.method == "POST":
        appointment = Appointment.objects.get(id = request.POST["id"], doctor = request.user.doctor)

        if appointment.status == Appointment.PREPARING:
            appointment.status = Appointment.READY
            appointment.save()

    appointments = Appointment.objects.filter(doctor = request.user.doctor).order_by("-id")
    return render(request, 'doctor/appointment.html', {"appointments": appointments})


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
