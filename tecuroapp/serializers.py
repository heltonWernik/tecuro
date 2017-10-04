from rest_framework import serializers

from tecuroapp.models import Doctor

class DoctorSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()

    def get_logo(self, doctor):
        request = self.context.get('request')
        logo_url = doctor.logo.url
        return request.build_absolute_uri(logo_url)

    class Meta:
        model = Doctor
        fields = ("id", "name", "phone", "address", "logo")
