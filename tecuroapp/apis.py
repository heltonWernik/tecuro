import json

from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from oauth2_provider.models import AccessToken

from tecuroapp.models import Doctor, Procedure, Appointment, AppointmentDetails
from tecuroapp.serializers import DoctorSerializer, ProcedureSerializer, AppointmentSerializer

def customer_get_doctors(request):
    doctors = DoctorSerializer(
        Doctor.objects.all().order_by("-id"),
        many = True,
        context = {"request": request}
    ).data

    return JsonResponse({"doctors": doctors})

def customer_get_procedures(request, doctor_id):
    procedures = ProcedureSerializer(
        Procedure.objects.filter(doctor_id = doctor_id).order_by("-id"),
        many = True,
        context = {"request": request}
    ).data

    return JsonResponse({"procedures": procedures})

@csrf_exempt
def customer_add_appointment(request):
    """
        params:
            access_token
            doctor_id
            address
            appointment_details (json format), example:
                [{"procedure_id": 1, "quantity": 2},{"procedure_id": 2, "quantity": 3}]
            stripe_token

        return:
            {"status": "success"}
    """

    if request.method == "POST":
        # Get token
        access_token = AccessToken.objects.get(token = request.POST.get("access_token"),
            expires__gt = timezone.now())

        # Get profile
        customer = access_token.user.customer

        # Check whether customer has any appointment that is not delivered
        if Appointment.objects.filter(customer = customer).exclude(status = Appointment.DELIVERED):
            return JsonResponse({"status": "failed", "error": "Your last appointment must be completed."})

        # Check Address
        if not request.POST["address"]:
            return JsonResponse({"status": "failed", "error": "Address is required."})

        # Get Appointment Details
        appointment_details = json.loads(request.POST["appointment_details"])

        appointment_total = 0
        for procedure in appointment_details:
            appointment_total += Procedure.objects.get(id = procedure["procedure_id"]).price * procedure["quantity"]

        if len(appointment_details) > 0:
            # Step 1 - Create an Appointment
            appointment = Appointment.objects.create(
                customer = customer,
                doctor_id = request.POST["doctor_id"],
                total = appointment_total,
                status = Appointment.PREPARING,
                address = request.POST["address"]
            )

            # Step 2 - Create Appointment details
            for procedure in appointment_details:
                AppointmentDetails.objects.create(
                    appointment = appointment,
                    procedure_id = procedure["procedure_id"],
                    quantity = procedure["quantity"],
                    sub_total = Procedure.objects.get(id = procedure["procedure_id"]).price * procedure["quantity"]
                )

            return JsonResponse({"status": "success"})


def customer_get_latest_appointment(request):
    access_token = AccessToken.objects.get(token = request.GET.get("access_token"),
        expires__gt = timezone.now())

    customer = access_token.user.customer
    appointment = AppointmentSerializer(Appointment.objects.filter(customer = customer).last()).data

    return JsonResponse({"appointment": appointment})


def doctor_appointment_notification(request, last_request_time):
    notification = Appointment.objects.filter(doctor = request.user.doctor,
        created_at__gt = last_request_time).count()

    return JsonResponse({"notification": notification})
