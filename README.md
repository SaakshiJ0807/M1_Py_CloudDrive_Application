Guide d'installation et de lancement du projet Django
Prérequis:
Python 3.x doit être installé.
pip (gestionnaire de paquets Python) doit être disponible.


Étapes d'installation


1. Créer un environnement virtuel
Ouvrez un terminal ou un invite de commande.

Naviguez dans le dossier du projet dézippé :
cd chemin/vers/DRIVE_PROJECT

Créez un environnement virtuel nommé cloud_drive_env :
python -m venv cloud_drive_env


2. Activer l'environnement virtuel

Sur Windows:
cloud_drive_env\Scripts\activate


3. Installer Django et les dépendances

Installez Django dans l'environnement virtuel :
pip install django


4. Appliquer les migrations

Initialisez la base de données avec les migrations :
python manage.py migrate



5. Lancer le serveur de développement

Démarrez le serveur pour tester l'application :
python manage.py runserver


Ensuite, accédez à l'application dans votre navigateur via cette URL :

http://127.0.0.1:8000/register/

C'est ici que l'expérience peut commencer !




