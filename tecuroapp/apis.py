from django.http import JsonResponse

from tecuroapp.models import Doctor
from tecuroapp.serializers import DoctorSerializer

def customer_get_doctors(request):
    doctors = DoctorSerializer(
        Doctor.objects.all().order_by("-id"),
        many = True,
        context = {"request": request}
    ).data

    return JsonResponse({"doctors": doctors})
