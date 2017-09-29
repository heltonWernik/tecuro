from django.contrib import admin

# Register your models here.
from tecuroapp.models import Doctor, Customer, Driver, Procedure

admin.site.register(Doctor)
admin.site.register(Customer)
admin.site.register(Driver)
admin.site.register(Procedure)
