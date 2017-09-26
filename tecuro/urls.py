from django.conf.urls import url
from django.contrib import admin
from tecuroapp import views
from django.contrib.auth import views as auth_views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name='home'),
    url(r'^doctor/sign-in/$', auth_views.login,
        {'template_name': 'doctor/sign_in.html'},
        name = 'doctor-sign-in'),
    url(r'^doctor/sign-out', auth_views.logout,
        {'next_page': '/'},
        name = 'doctor-sign-out'),
    url(r'^doctor/sign-up', views.doctor_sign_up,
        name = 'doctor-sign-up'),
    url(r'^doctor/$', views.doctor_home, name = 'doctor-home')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
