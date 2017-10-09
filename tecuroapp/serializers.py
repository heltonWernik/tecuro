from rest_framework import serializers

from tecuroapp.models import Doctor, \
    Procedure, \
    Customer, \
    Driver, \
    Appointment, \
    AppointmentDetails

class DoctorSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()

    def get_logo(self, doctor):
        request = self.context.get('request')
        logo_url = doctor.logo.url
        return request.build_absolute_uri(logo_url)

    class Meta:
        model = Doctor
        fields = ("id", "name", "phone", "address", "logo")

class ProcedureSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, procedure):
        request = self.context.get('request')
        image_url = procedure.image.url
        return request.build_absolute_uri(image_url)

    class Meta:
        model = Procedure
        fields = ("id", "name", "short_description", "image", "price")

# ORDER SERIALIZER
class AppointmentCustomerSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source="user.get_full_name")

    class Meta:
        model = Customer
        fields = ("id", "name", "avatar", "phone", "address")

class AppointmentDriverSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source="user.get_full_name")

    class Meta:
        model = Customer
        fields = ("id", "name", "avatar", "phone", "address")

class AppointmentDoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ("id", "name", "phone", "address")

class AppointmentProcedureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Procedure
        fields = ("id", "name", "price")

class AppointmentDetailsSerializer(serializers.ModelSerializer):
    procedure = AppointmentProcedureSerializer()

    class Meta:
        model = AppointmentDetails
        fields = ("id", "procedure", "quantity", "sub_total")

class AppointmentSerializer(serializers.ModelSerializer):
    customer = AppointmentCustomerSerializer()
    driver = AppointmentDriverSerializer()
    doctor = AppointmentDoctorSerializer()
    appointment_details = AppointmentDetailsSerializer(many = True)
    status = serializers.ReadOnlyField(source = "get_status_display")

    class Meta:
        model = Appointment
        fields = ("id", "customer", "doctor", "driver", "appointment_details", "total", "status", "address")
