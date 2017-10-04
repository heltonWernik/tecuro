from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

from tecuroapp import views, apis

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name='home'),

    # Doctor
    url(r'^doctor/sign-in/$', auth_views.login,
        {'template_name': 'doctor/sign_in.html'},
        name = 'doctor-sign-in'),
    url(r'^doctor/sign-out', auth_views.logout,
        {'next_page': '/'},
        name = 'doctor-sign-out'),
    url(r'^doctor/sign-up', views.doctor_sign_up,
        name = 'doctor-sign-up'),
    url(r'^doctor/$', views.doctor_home, name = 'doctor-home'),

    url(r'^doctor/account/$', views.doctor_account, name = 'doctor-account'),
    url(r'^doctor/procedure/$', views.doctor_procedure, name = 'doctor-procedure'),
    url(r'^doctor/procedure/add/$', views.doctor_add_procedure, name = 'doctor-add-procedure'),

    url(r'^doctor/procedure/edit/(?P<procedure_id>\d+)/$', views.doctor_edit_procedure, name = 'doctor-edit-procedure'),

    url(r'^doctor/appointment/$', views.doctor_appointment, name = 'doctor-appointment'),
    url(r'^doctor/report/$', views.doctor_report, name = 'doctor-report'),

    #Sign Up/ Sign In/ Sign Up
    url(r'^api/social/', include('rest_framework_social_oauth2.urls')),
    # /convert-token (sign in/ sign up)
    # /revoke-token (sign out)

    url(r'^api/customer/doctors/$', apis.customer_get_doctors),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
