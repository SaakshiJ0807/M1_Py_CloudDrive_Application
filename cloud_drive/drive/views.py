from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from .form import LoginForm, RegisterForm # Make sure LoginForm is defined in forms.py
from django.contrib.auth.decorators import login_required
import os
from django.conf import settings
from datetime import datetime
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.shortcuts import render
from datetime import datetime
from django.http import Http404
from urllib.parse import unquote
from .models import UserStorage  # Importatiion UserStorage pour le stockage de l'utilisateur


FILE_TYPES = {
    'txt': {'description': 'Fichier texte', 'icon': 'bi-file-text'},
    'pdf': {'description': 'Document PDF', 'icon': 'bi-file-earmark-pdf'},
    'doc': {'description': 'Document Word', 'icon': 'bi-file-earmark-word'},
    'docx': {'description': 'Document Word', 'icon': 'bi-file-earmark-word'},
    'xls': {'description': 'Feuille de calcul Excel', 'icon': 'bi-file-earmark-spreadsheet'},
    'xlsx': {'description': 'Feuille de calcul Excel', 'icon': 'bi-file-earmark-spreadsheet'},
    'ppt': {'description': 'Présentation PowerPoint', 'icon': 'bi-file-earmark-ppt'},
    'pptx': {'description': 'Présentation PowerPoint', 'icon': 'bi-file-earmark-ppt'},
    'jpg': {'description': 'Image JPEG', 'icon': 'bi-file-earmark-image'},
    'jpeg': {'description': 'Image JPEG', 'icon': 'bi-file-earmark-image'},
    'png': {'description': 'Image PNG', 'icon': 'bi-file-earmark-image'},
    'gif': {'description': 'Image GIF', 'icon': 'bi-file-earmark-image'},
    'bmp': {'description': 'Image BMP', 'icon': 'bi-file-earmark-image'},
    'mp3': {'description': 'Fichier audio MP3', 'icon': 'bi-file-earmark-music'},
    'wav': {'description': 'Fichier audio WAV', 'icon': 'bi-file-earmark-music'},
    'mp4': {'description': 'Vidéo MP4', 'icon': 'bi-file-earmark-play'},
    'avi': {'description': 'Vidéo AVI', 'icon': 'bi-file-earmark-play'},
    'mkv': {'description': 'Vidéo MKV', 'icon': 'bi-file-earmark-play'},
    'zip': {'description': 'Archive ZIP', 'icon': 'bi-file-earmark-zip'},
    'rar': {'description': 'Archive RAR', 'icon': 'bi-file-earmark-zip'},
    '7z': {'description': 'Archive 7z', 'icon': 'bi-file-earmark-zip'},
    'html': {'description': 'Fichier HTML', 'icon': 'bi-file-earmark-code'},
    'css': {'description': 'Fichier CSS', 'icon': 'bi-file-earmark-code'},
    'js': {'description': 'Fichier JavaScript', 'icon': 'bi-file-earmark-code'},
    'py': {'description': 'Script Python', 'icon': 'bi-file-earmark-code'},
    'java': {'description': 'Code source Java', 'icon': 'bi-file-earmark-code'},
    'c': {'description': 'Code source C', 'icon': 'bi-file-earmark-code'},
    'cpp': {'description': 'Code source C++', 'icon': 'bi-file-earmark-code'},
    'json': {'description': 'Fichier JSON', 'icon': 'bi-file-earmark-code'},
    'xml': {'description': 'Fichier XML', 'icon': 'bi-file-earmark-code'},
}


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Créer un dossier pour l'utilisateur
            user_folder = os.path.join(settings.BASE_DIR, 'user_files', user.username)
            os.makedirs(user_folder, exist_ok=True)
            UserStorage.objects.create(user=user, used_space=0, total_space=100 * 1024 * 1024)
            return redirect('login')  # Assurez-vous que 'login' correspond à votre URL nommée pour la page de connexion)
    else:
        form = RegisterForm()
    return render(request, "drive/register.html", {"form": form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirection vers la page d'accueil après connexion
    else:
        form = LoginForm()
    return render(request, 'drive/login.html', {'form': form})  # Assurez-vous que ce chemin est correct


def logout_view(request):
    logout(request)
    return redirect('login')  # Redirection vers la page de connexion après déconnexion


@login_required
def home(request):
    return render(request, "drive/home.html")


@login_required
def cloud_view(request, path=''):
    base_folder = os.path.join(settings.BASE_DIR, 'user_files', request.user.username)
    current_path = request.GET.get('path', '')
    current_path = unquote(current_path).lstrip('/')
    user_folder = os.path.normpath(os.path.join(base_folder, current_path))

    # Vérification des chemins pour la sécurité
    if not os.path.exists(user_folder) or os.path.commonpath([base_folder, user_folder]) != base_folder:
        raise Http404("Dossier introuvable")

    content = []
    for item in os.listdir(user_folder):
        item_path = os.path.join(user_folder, item)
        is_dir = os.path.isdir(item_path)
        
        # Récupération de l'extension et de l'icône
        ext = os.path.splitext(item)[1][1:].lower()
        file_info = {
            'name': item,
            'is_dir': is_dir,
            'modified': datetime.fromtimestamp(os.path.getmtime(item_path)).strftime('%Y-%m-%d'),
            'size': f"{round(os.path.getsize(item_path) / (1024 * 1024), 2)} MB" if not is_dir else None,
            'type': 'Dossier' if is_dir else FILE_TYPES.get(ext, {}).get('description', 'Fichier'),
            'icon': 'bi-folder-fill' if is_dir else FILE_TYPES.get(ext, {}).get('icon', 'bi-file-earmark')
        }
        #file_info['file_path'] = os.path.join(current_path, item) 
        #content.append(file_info)

      
        file_info['file_path'] = f"{current_path}/{item}".replace("\\", "/")  
        content.append(file_info)

    return render(request, 'drive/cloud.html', {'content': content, 'current_path': current_path})

# Fonction pour calculer la taille totale d'un dossier en MB
def get_folder_size(folder_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return round(total_size / (1024 * 1024), 2)  # Taille en MB


import os
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

def check_user_folder_size(user_folder):
    total_size = 0
    for dirpath, _, filenames in os.walk(user_folder):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size <= 100 * 1024 * 1024  # Limite de 100 MB


@login_required
def rename_file(request, file_path):
    # Décoder et normaliser le chemin

    if file_path.startswith('/'):
    # Supprime la barre oblique du début du chemin
        file_path = file_path[1:]

    file_path = unquote(file_path)
    file_path = os.path.normpath(file_path)

    base_folder = os.path.join(settings.BASE_DIR, 'user_files', request.user.username)
    full_file_path = os.path.join(base_folder, file_path)

    # Vérification de sécurité pour s'assurer que le chemin est bien dans le répertoire de l'utilisateur
    if not full_file_path.startswith(base_folder) or not os.path.exists(full_file_path):
        return JsonResponse({'success': False, 'error': "Fichier ou dossier introuvable."})

    # Obtenez le nouveau nom
    new_name = request.POST.get('new_name')
    new_file_path = os.path.join(os.path.dirname(full_file_path), new_name)

    try:
        os.rename(full_file_path, new_file_path)
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    

import shutil
from django.http import JsonResponse

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
import os
import shutil
from django.conf import settings
from urllib.parse import unquote

@login_required
@require_POST
def duplicate_file(request, file_path):
    # Décoder le chemin du fichier
    #file_path = unquote(file_path)

    # Décodage et normalisation du chemin
    file_path = os.path.normpath(file_path)

    if file_path.startswith('\\'):
         # Supprime la barre oblique inversée du début du chemin
        file_path = file_path[1:]
        print("test")

    print(file_path)

    # Définir le dossier de base de l'utilisateur
    base_folder = os.path.join(settings.BASE_DIR, 'user_files', request.user.username)
    full_file_path = os.path.normpath(os.path.join(base_folder, file_path))

    # Vérification de sécurité
    if not full_file_path.startswith(base_folder):
        return JsonResponse({'success': False, 'error': "Accès non autorisé."})

    # Vérification de l'existence du fichier
    if not os.path.exists(full_file_path):
        return JsonResponse({'success': False, 'error': "Fichier introuvable."})

    # Génération d'un nouveau nom de fichier pour la copie
    base, ext = os.path.splitext(full_file_path)
    copy_number = 1
    new_file_path = f"{base} (Copie{copy_number}){ext}"
    
    while os.path.exists(new_file_path):
        copy_number += 1
        new_file_path = f"{base} (Copie{copy_number}){ext}"


    # Duplication du fichier
    try:
        if os.path.isfile(full_file_path):
            shutil.copy2(full_file_path, new_file_path)
            copied_size = os.path.getsize(new_file_path)

             # Mettre à jour la taille de l'espace de stockage utilisé
            user_storage, created = UserStorage.objects.get_or_create(user=request.user)
            user_storage.used_space += copied_size
            user_storage.save()


        elif os.path.isdir(full_file_path):
            shutil.copytree(full_file_path, new_file_path)
            copied_size = get_folder_size(new_file_path)  # Fonction pour calculer la taille d'un dossier
            user_storage, created = UserStorage.objects.get_or_create(user=request.user)
            user_storage.used_space += copied_size
            user_storage.save()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})




import os
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required


from pathlib import Path
import shutil
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
import subprocess



from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required



import subprocess
from pathlib import Path
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.conf import settings
import urllib.parse




@login_required
@require_POST
def delete_file(request, file_path):
    # Décodage et normalisation du chemin
    file_path = os.path.normpath(file_path)
    
    if file_path.startswith('\\') or file_path.startswith('/'):
        # Supprime les barres obliques ou obliques inversées du début
        file_path = file_path[1:]

    # Définir le dossier de base de l'utilisateur
    base_folder = os.path.join(settings.BASE_DIR, 'user_files', request.user.username)
    full_file_path = os.path.normpath(os.path.join(base_folder, file_path))

    # Vérification de sécurité
    if not full_file_path.startswith(base_folder):
        return JsonResponse({'success': False, 'error': "Accès non autorisé."})

    # Vérification de l'existence du fichier ou dossier
    if not os.path.exists(full_file_path):
        return JsonResponse({'success': False, 'error': "Fichier ou dossier introuvable."})

    try:
        if os.path.isfile(full_file_path):
            file_size = os.path.getsize(full_file_path)
            os.remove(full_file_path)  # Suppression du fichier
        elif os.path.isdir(full_file_path):
            file_size = get_folder_size(full_file_path)
            shutil.rmtree(full_file_path)  # Suppression du dossier

        # Mise à jour de l'espace utilisé dans la base de données
        user_storage, created = UserStorage.objects.get_or_create(user=request.user)
        user_storage.used_space -= file_size
        user_storage.used_space = max(user_storage.used_space, 0)  # Empêcher une valeur négative
        user_storage.save()

        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})



import os
from django.conf import settings
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required


@login_required
def create_folder(request):
    if request.method == "POST":
        folder_name = request.POST.get('folder_name')
        current_path = request.POST.get('current_path', '')
        base_folder = os.path.join(settings.BASE_DIR, 'user_files', request.user.username)
        folder_path = os.path.join(base_folder, current_path, folder_name)
        
        try:
            os.makedirs(folder_path)
            # Redirection vers le répertoire actuel
            return HttpResponseRedirect(reverse('cloud_view') + f"?path={current_path}")
        except FileExistsError:
            return JsonResponse({'success': False, 'error': "Un dossier avec ce nom existe déjà."})
        except PermissionError:
            return JsonResponse({'success': False, 'error': "Permission refusée pour créer le dossier."})

        
from django.shortcuts import get_object_or_404
from .models import UserStorage

from django.shortcuts import get_object_or_404
from .models import UserStorage


from django.shortcuts import redirect
from .models import UserStorage
from django.http import JsonResponse
from django.conf import settings
from django.core.files.storage import default_storage
import os

@login_required
def upload_file(request):
    if request.method == "POST" and request.FILES.get('file'):
        file = request.FILES['file']
        file_size = file.size  # Taille en octets

        # Récupérer ou créer l'entrée UserStorage pour l'utilisateur
        user_storage, created = UserStorage.objects.get_or_create(user=request.user)

        print(user_storage.total_space)

        # Vérifier si la taille du fichier dépasse la limite de 40 MB
        if file_size > 40 * 1024 * 1024:
            return JsonResponse({'success': False, 'error': "Chaque fichier ne doit pas dépasser 40 MB."})

        # Vérifier l'espace total pour l'utilisateur
        if user_storage.used_space + file_size > user_storage.total_space:
            return JsonResponse({'success': False, 'error': "Espace insuffisant. Votre espace de stockage total ne doit pas dépasser 100 MB."})

        # Enregistrer le fichier dans le répertoire actuel
        base_folder = os.path.join(settings.BASE_DIR, 'user_files', request.user.username)
        current_path = request.POST.get('current_path', '')  # Récupérer `current_path` ou valeur par défaut
        file_path = os.path.join(base_folder, current_path, file.name)
        print(file_path)

        os.makedirs(os.path.dirname(file_path), exist_ok=True)  # Crée le répertoire si nécessaire
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        # Mettre à jour l'espace utilisé dans la base de données
        user_storage.used_space += file_size
        user_storage.save()

        # Redirection en utilisant `current_path`, même si c'est une chaîne vide
        if current_path:
            redirect_path = reverse('cloud_view', kwargs={'path': current_path})
        else:
            redirect_path = reverse('cloud_view')

        return HttpResponseRedirect(redirect_path)
    else:
        return JsonResponse({'success': False, 'error': "Aucun fichier sélectionné."})
    


@login_required
def home(request):
    # Récupérer l'objet de stockage de l'utilisateur actuel
    user_storage = UserStorage.objects.get(user=request.user)

    # Calcul du pourcentage d'utilisation
    used_space = user_storage.used_space / (1024 * 1024)  # Convertir en MB
    total_space = user_storage.total_space / (1024 * 1024)  # Convertir en MB
    percentage_used = (used_space / total_space) * 100

    context = {
        'used_space': used_space,
        'total_space': total_space,
        'percentage_used': percentage_used
    }
    return render(request, "drive/home.html", context)



# Fonction pour calculer la taille totale d'un dossier en MB
def get_folder_size(folder_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return round(total_size / (1024 * 1024), 2)  # Taille en MB



from django.shortcuts import render
from django.http import HttpResponse, FileResponse
def preview_file(request, file_path):
    if file_path.startswith('\\') or file_path.startswith('/'):
        # Supprime les barres obliques ou obliques inversées du début
        file_path = file_path[1:]
    
    base_folder = os.path.join(settings.BASE_DIR, 'user_files', request.user.username)
    full_file_path = os.path.normpath(os.path.join(base_folder, file_path))
    
    # Vérification de sécurité
    if not full_file_path.startswith(base_folder) or not os.path.exists(full_file_path):
        return HttpResponse("Fichier introuvable", status=404)
    
    # Renvoie le fichier directement dans une réponse ou utilise un rendu spécifique
    return FileResponse(open(full_file_path, 'rb'))



















