from django.contrib import admin
import src
from src import authenticator
from src.authenticator import urls
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
]
