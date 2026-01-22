from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),  # Page d'accueil
    path('register/', views.register_view, name='register'),  # Inscription
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('cloud/', views.cloud_view, name='cloud'),  # URL pour accéder au cloud
    path('cloud/<path:path>/', views.cloud_view, name='cloud_view'),

    #path('rename/', views.rename_file, name='rename_file'),    # URL pour renommer
    #path('duplicate/', views.duplicate_file, name='duplicate_file'),  # URL pour dupliquer
    #path('delete/', views.delete_file, name='delete_file'),     # URL pour supprimer

    path('delete/<path:file_path>/', views.delete_file, name='delete_file'),
    path('rename/<path:file_path>/', views.rename_file, name='rename_file'),
    path('duplicate/<path:file_path>/', views.duplicate_file, name='duplicate_file'),

    path('create_folder/', views.create_folder, name='create_folder'),
    path('upload_file/', views.upload_file, name='upload_file'),
    path('', views.cloud_view, name='cloud_view'),
    path('preview/<path:file_path>/', views.preview_file, name='preview_file'),
    # autres URLs
]



