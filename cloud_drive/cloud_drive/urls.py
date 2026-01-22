# cloud_drive/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # Connexion/Déconnexion
    path('', include('drive.urls')),  # Inclusion des URLs de l'application drive
]