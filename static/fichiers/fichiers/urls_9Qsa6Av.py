from django.urls import path
from . import views

app_name = "accounts"  # ce nom sera utilise pour creer des liens dans le but d'eviter les conflits de noms

urlpatterns = [
    path('connexion/', views.connexion, name="connexion"),
    path('', views.inscription, name="inscription"),
   
    path('home/', views.home, name="home"),
    path('client/', views.client, name="client"),
    path('commande/', views.commande, name="commande"),

    path('liste_commande/', views.liste_commande, name="liste_commande"),
   # path('<int:commande_id>/', views.show, name="show"),
   # path('ajouter_commande/', views.ajouter_commande, name="ajouter_commande"),
    path('modifier_commande/<int:commande_id>/', views.modifier_commande, name="modifier_commande"),
    path('supprimer_commande/<int:commande_id>/', views.supprimer_commande, name="supprimer_commande"), # Suppression d'une commande par rapport a son id
    path('commande<int:facture_id>/', views.facture, name="facture"), # Facture d'une commande
#    path('profil', views.commandes_de_chaque_client, name="commandes_de_chaque_client"), # Facture d'une commande
    path('client/<int:profil_id>/', views.profil, name="profil")






    


]