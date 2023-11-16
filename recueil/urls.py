
from django.urls import path
from . import views
#from .views import *


app_name = 'recueil'
urlpatterns  = [



    path('', views.connexion, name="connexion"),
    path('inscription', views.inscription, name="inscription"),
    path('deconnexion', views.deconnexion, name="deconnexion"),
    path("renitialiser/", views.renitialiser, name="renitialiser"),
    path('nouveauPasse/<str:uidb64>/<str:token>/', views.nouveauPasse, name="nouveauPasse"),

    # Urls pour University
    path('university', views.university, name='university'),
    path('universityList', views.universityList, name='universityList'),
    path('modifierUniversity/<int:university_id>/', views.modifierUniversity, name='modifierUniversity'),
    path('supprimerUniversity/<int:university_id>/', views.supprimerUniversity, name='supprimerUniversity'),
    path('ufr_par_university/<int:university_id>/', views.ufr_par_university, name='ufr_par_university'),



    # Urls pour UFR
    path('ufr', views.ufr, name='ufr'),
    path('ufrList', views.ufrList, name='ufrList'),
    path('modifierUfr/<int:ufr_id>/', views.modifierUfr, name='modifierUfr'),
    path('supprimerUfr/<int:ufr_id>/', views.supprimerUfr, name='supprimerUfr'),
    path('filiere_par_ufr/<int:ufr_id>/', views.filiere_par_ufr, name='filiere_par_ufr'),



    # Urls pour Filiere
    path('filiere', views.filiere, name='filiere'),
    path('filiereList', views.filiereList, name='filiereList'),
    path('modifierFiliere/<int:filiere_id>/', views.modifierFiliere, name='modifierFiliere'),
    path('supprimerFiliere/<int:filiere_id>/', views.supprimerFiliere, name='supprimerFiliere'),
    path('niveau_par_filiere/<int:filiere_id>/', views.niveau_par_filiere, name='niveau_par_filiere'),


    # Urls pour Year ou niveaux
    path('yearList', views.yearList, name='yearList'),
    path('year', views.year, name='year'),
    path('modifierYear/<int:year_id>/', views.modifierYear, name='modifierYear'),
    path('supprimerYear/<int:year_id>/', views.supprimerYear, name='supprimerYear'),

    # Urls pour Semestre
    path('semestre/', views.semestre, name='semestre'),
    path('semestreList/liste', views.semestreList, name='semestreList'),
    path('modfifierSemestre/<int:semestre_id>/', views.modfifierSemestre, name='modfifierSemestre'),
    path('supprimerSemestre/<int:semestre_id>/', views.supprimerSemestre, name='supprimerSemestre'),

    # Urls pour Module
    path('module/', views.module, name='module'),
    path('moduleList/liste', views.moduleList, name='moduleList'),
    path('modifierModule/<int:module_id>/', views.modifierModule, name='modifierModule'),
    path('supprimerModule/<int:module_id>/', views.supprimerModule, name='supprimerModule'),

    # Urls pour Fichier
    path('fichier/', views.fichier, name='fichier'),
    path('fichier/liste', views.fichierList, name='fichierList'),
    path('modifierFichier/<int:fichier_id>/', views.modifierFichier, name='modifierFichier'),
    path('supprimerFichier/<int:fichier_id>/', views.supprimerFichier, name='supprimerFichier'),

    path('semeste_par_niveau/<int:year_id>/', views.semeste_par_niveau, name='semeste_par_niveau'),
    path('module_par_semestre/<int:semestre_id>/', views.module_par_semestre, name='module_par_semestre'),
    path('cours_par_modules/<int:module_id>/', views.cours_par_modules, name='cours_par_modules'),



    path('test', views.adama)






]