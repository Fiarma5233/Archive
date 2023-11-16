from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.db import IntegrityError
from .models import Couturier, Client, Commande, Facture
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.



def home(request):
    if request.method == 'GET':
        dir = {
           "greeting": "Vous etes la bienvenue"
        }
        return render(request, "accounts/Home.html")
#    return render(request, "accounts/Home.html", dir)

def inscription(request):
    if request.method =="GET":

        contexte = {
            "titre1": "Inscription",
            "message" : "Bonsoir",
            }
        return render (request, "accounts/Inscription.html")
    
    '''
    Lastname = request.POST.get('Lastname')
    Firstname = request.POST.get('Firstname')
    Company = request.POST.get("Company")
    Email = request.POST.get("Email")
    Password = request.POST.get("Password")
    PasswordConfirm = request.POST.get(" PasswordConfirm")
    couturier = Couturier.objects.create(Lastname=Lastname ,  Firstname=Firstname, Company=Company, Email=Email, Password=Password, PasswordConfirm=PasswordConfirm )                   # Appel de notre model
    couturier.save() # Enregistrement de nos donnees dans la db

    '''
    
    if request.method == 'POST':
    # Recuperation des donnees entrees par l'utilisateur
        Lastname = request.POST.get('Lastname')
       
        Firstname = request.POST.get('Firstname')
        Company = request.POST.get("Company")
        Email = request.POST.get("Email")
        Password = request.POST.get("Password")
        PasswordConfirm = request.POST.get(" PasswordConfirm")
        couturier = Couturier.objects.create(Lastname=Lastname ,  Firstname=Firstname, Company=Company, Email=Email, Password=Password, PasswordConfirm=PasswordConfirm )                   # Appel de notre model
        couturier.save() # Enregistrement de nos donnees dans la db
        messages.success(request, 'Votre compte a ete creee avec succes')
        return redirect('accounts:connexion')

                             
    return render(request, "accounts/Inscription.html", contexte)

def connexion(request):
    '''if request.method == "GET":
        return render (request, "accounts/Connexion.html")
    msg = {
        "salut" :"Vous etes connectes"
    }'''

    '''if request.method == "POST":
        Company = request.POST.get("Company")
        Password = request.POST.get("Password")
        # verification avec la methode 
        user = authenticate(Company=Company, Password=Password)

        # Verifions si l'utilisateur existe 
        if user is not None:
            login(request, user)
            firstname = Couturier.Firstname
            return render( request, "accounts/Home.html", {"firstname" : firstname})
        else:
            messages.error(request, "Mauvaise authentification")
            return redirect('accounts:connexion')'''
    
    if request.method == "POST":
        Company = request.POST["Company"]
        Password = request.POST["Password"]
        # verification avec la methode 
        user = authenticate(Company=Company, Password=Password)

        # Verifions si l'utilisateur existe 
        if user is not None:
            login(request, user)
            firstname = Couturier.Firstname
            return  redirect("accounts:home") #render(request, "accounts/Home.html", {"firstname" : firstname})
        else:
            messages.error(request, "Mauvaise authentification")
            return redirect('accounts:connexion')
    return render(request, 'accounts/Connexion.html')

# Recuperation des donnees du Client
def client(request):
    if request.method =="GET":
        '''if request.method == "GET":
            return render(request, "accounts/Client.html") 
        
        if request.method == "POST":
            Nom = request.POST.get("Nom")
            #Prenom = request.POST.get("Prenom")
            Telephone = request.POST.get("Telephone")
            client = Client.objects.create(Nom=Nom,  Telephone=Telephone)
            client.save()
            msg = messages.success(request, "Inscription reussie")
            return redirect('accounts:commande')'''
        clients =  Client.objects.all()
        return render(request, 'accounts/Client.html', {"clients": clients})




# Recuperation des donnees de la  commande
def commande(request):
    if request.method == "GET":
        client = Client.objects.all()
        contest = { ' clients ' : client}
        return render(request, "accounts/Commande.html", contest)
    
    if request.method == "POST":
        
        Nom = request.POST.get("Nom")
        Telephone = request.POST.get("Telephone")
        #Client = request.POST.get("Client")
        Modele_Couture = request.POST.get("Modele_Couture")
        Nombre_Pagnes = request.POST.get("Nombre_Pagnes")
        Dos = request.POST.get("Dos")
        Epaule = request.POST.get("Epaule")
        Poitrine = request.POST.get("Poitrine")
        Longueur_Manche = request.POST.get("Longueur_Manche")
        Tour_Manche = request.POST.get("Tour_Manche")
        Longueur_Taille = request.POST.get("Longueur_Taille")
        Tour_Taille = request.POST.get("Tour_Taille")
        Pince_longueur_seins = request.POST.get("Pince_longueur_seins")
        Longueur_Camisole = request.POST.get("Longueur_Camisole")
        Longueur_Robe = request.POST.get("Longueur_Robe")
        Longueur_Chemise = request.POST.get("Longueur_Chemise")
        Messure_Bassin = request.POST.get("Messure_Bassin")
        Mesure_Ceinture = request.POST.get("Mesure_Ceinture")
        Mesure_Cuisse = request.POST.get("Mesure_Cuisse")
        Mesure_Genoux = request.POST.get("Mesure_Genoux")
        Longeur_Jupe = request.POST.get("Longeur_Jupe")
        Longueur_Bras = request.POST.get("Longueur_Bras")
        Longueur_Poignet = request.POST.get("Longueur_Poignet")
        Prix_Couture = request.POST.get("Prix_Couture")
        Avance = request.POST.get("Avance")
        Date_Depot_Model = request.POST.get("Date_Depot_Model")
        Date_Retrait_Model = request.POST.get("Date_Retrait_Model")

        # verifions si le client existe
        try:
            
            client = Client.objects.get(Telephone=Telephone)
            #client.Interventions += 1
            Client.Nom=Nom
            client.save()
        
        except Client.DoesNotExist:
            try:
                client = Client.objects.create(Nom=Nom, Telephone=Telephone, Interventions=0)
                client.save()

            except IntegrityError:
                client=  Client.objects.get(Telephone=Telephone)
        '''Facture.Solde =0
        facture = Facture.objects.create(
            Nom=Nom,
            Telephone=Telephone,
            Modele_couture=Modele_Couture,
            Prix_Couture=Prix_Couture,
            Avance=Avance,
            Solde=Commande.Prix_Couture - Commande.Avance
            

        )
        facture.save()'''
        commande = Commande.objects.create(client=client, Nom=Nom, Telephone=Telephone, Modele_Couture=Modele_Couture, Nombre_Pagnes=Nombre_Pagnes, Dos=Dos, Epaule=Epaule, Poitrine=Poitrine, Longueur_Manche=Longueur_Manche, Tour_Manche=Tour_Manche , Longueur_Taille=Longueur_Taille, Tour_Taille=Tour_Taille, Pince_longueur_seins=Pince_longueur_seins, Longueur_Camisole=Longueur_Camisole, Longueur_Robe=Longueur_Robe, Longueur_Chemise=Longueur_Chemise, Messure_Bassin=Messure_Bassin, Mesure_Ceinture=Mesure_Ceinture, Mesure_Cuisse=Mesure_Cuisse, Mesure_Genoux=Mesure_Genoux, Longeur_Jupe=Longeur_Jupe, Longueur_Bras=Longueur_Bras, Longueur_Poignet=Longueur_Poignet, Prix_Couture=Prix_Couture, Avance=Avance, Date_Depot_Model=Date_Depot_Model, Date_Retrait_Model=Date_Retrait_Model)
        
        commande.save()
        client.Interventions += 1
        client.save()

        
# Creation d'une facture
        Prix_Couture=float(request.POST.get('Prix_Couture'))  # Pour convertir les valeur qui sont de type string en float afin d'effecturerles operations(calcul du solde)
        Avance=float(request.POST.get('Avance'))
        Solde=Prix_Couture - Avance
        

        
        # Creation de facture
        #Solde = 0
        #Solde = Commande.Prix_Couture - Commande.Avance
        #commande = Commande.objects.get(Telephone)
        #Solde=int(commande.Prix_Couture) - int(commande.Avance)

        facture = Facture.objects.create(
            command=commande,
            Nom=Nom,
            Telephone=Telephone,
            Modele_couture=Modele_Couture,
            Prix_Couture=Prix_Couture,
            Avance=Avance,
            Solde=Solde

        )
        facture.save()
        messages.success(request, "Commande ajoutee avec succes")
        return redirect('accounts:liste_commande')
   

    return render(request, "accounts/Commande.html") 


'''def commande(request):
    if request.method == "GET":
        client = Client.objects.all()
        contest = { ' clients ' : client}
        return render(request, "accounts/Commande.html", contest)
    
    if request.method == "POST":
        
        Nom = request.POST.get("Nom")
        Telephone = request.POST.get("Telephone")
        #Client = request.POST.get("Client")
        Modele_Couture = request.POST.get("Modele_Couture")
        Nombre_Pagnes = request.POST.get("Nombre_Pagnes")
        Dos = request.POST.get("Dos")
        Epaule = request.POST.get("Epaule")
        Poitrine = request.POST.get("Poitrine")
        Longueur_Manche = request.POST.get("Longueur_Manche")
        Tour_Manche = request.POST.get("Tour_Manche")
        Longueur_Taille = request.POST.get("Longueur_Taille")
        Tour_Taille = request.POST.get("Tour_Taille")
        Pince_longueur_seins = request.POST.get("Pince_longueur_seins")
        Longueur_Camisole = request.POST.get("Longueur_Camisole")
        Longueur_Robe = request.POST.get("Longueur_Robe")
        Longueur_Chemise = request.POST.get("Longueur_Chemise")
        Messure_Bassin = request.POST.get("Messure_Bassin")
        Mesure_Ceinture = request.POST.get("Mesure_Ceinture")
        Mesure_Cuisse = request.POST.get("Mesure_Cuisse")
        Mesure_Genoux = request.POST.get("Mesure_Genoux")
        Longeur_Jupe = request.POST.get("Longeur_Jupe")
        Longueur_Bras = request.POST.get("Longueur_Bras")
        Longueur_Poignet = request.POST.get("Longueur_Poignet")
        Prix_Couture = request.POST.get("Prix_Couture")
        Avance = request.POST.get("Avance")
        Date_Depot_Model = request.POST.get("Date_Depot_Model")
        Date_Retrait_Model = request.POST.get("Date_Retrait_Model")

        #    Chercher le client existant ou en creer dans le cas contraire
        Interventions = Client.Interventions = 1 
        client, created =  Client.objects.get_or_create( Telephone=Telephone, defaults={ 'Nom':Nom, "Interventions":Interventions} )
        # Si le client existe deja on incremente
        if not created:
            Client.Interventions +=1
            client.save()
        
        commande = Commande.objects.create(client=client,Nom=Nom, Telephone=Telephone, Modele_Couture=Modele_Couture, Nombre_Pagnes=Nombre_Pagnes, Dos=Dos, Epaule=Epaule, Poitrine=Poitrine, Longueur_Manche=Longueur_Manche, Tour_Manche=Tour_Manche , Longueur_Taille=Longueur_Taille, Tour_Taille=Tour_Taille, Pince_longueur_seins=Pince_longueur_seins, Longueur_Camisole=Longueur_Camisole, Longueur_Robe=Longueur_Robe, Longueur_Chemise=Longueur_Chemise, Messure_Bassin=Messure_Bassin, Mesure_Ceinture=Mesure_Ceinture, Mesure_Cuisse=Mesure_Cuisse, Mesure_Genoux=Mesure_Genoux, Longeur_Jupe=Longeur_Jupe, Longueur_Bras=Longueur_Bras, Longueur_Poignet=Longueur_Poignet, Prix_Couture=Prix_Couture, Avance=Avance, Date_Depot_Model=Date_Depot_Model, Date_Retrait_Model=Date_Retrait_Model)
        
        commande.save()

        # verifions si le client existe
        'try:
            Client.Interventions =0
            client = Client.objects.filter(Telephone=Telephone)
            Client.Interventions += 1
            client.save()
        
        except Client.DoesNotExist:
           
            client = Client.objects.create(Nom=Nom, Telephone=Telephone, Interventions=1)
            client.save()

        # Creation de facture
        #Solde = 0
        #Solde = Commande.Prix_Couture - Commande.Avance
        #commande = Commande.objects.get(Telephone)
        Solde=int(commande.Prix_Couture) - int(commande.Avance)

        facture = Facture.objects.create(
            Nom=Nom,
            Telephone=Telephone,
            Modele_couture=Modele_Couture,
            Prix_Couture=Prix_Couture,
            Avance=Avance,
            Solde=Solde

        )
        facture.save()''
        messages.success(request, "Commande ajoutee avec succes")
        return redirect('accounts:liste_commande')
   

    return render(request, "accounts/Commande.html")
'''

  
# Liste des commandes
def liste_commande(request):
    cmd = { 'commandes' : Commande.objects.all()}
    return render(request, 'accounts/ListeCommande.html', cmd)

#def show(request, Telephone):
    #client = Client.objects.get(Telephone=Telephone)
    #commandes = Commande.objects.filter(client=client)
    '''com = {
               "client" :get_object_or_404(Client, Telephone=Telephone),
               'commandes' : client.Commande.all() 
               
    }'''
    #return render(request, "accounts/Show.html", {'client': client, "commandes":commandes})


# Facture

def facture(request, facture_id):
    fact = {'factures': Facture.objects.all(Facture, pk=facture_id)}
    return render(request, 'accounts/Facture.html', fact)
# Ajouter une commande

def ajouter_commande(request):
    client = Client.objects.get()  # recuperation des clients

# Modification d'une commande
def modifier_commande(request, commande_id):
    if request.method == "GET":
        commande = get_object_or_404(Commande, id=commande_id)
        #commande = Commande.objects.filter(id=commande_id)
        contex = {'commande' : commande}
       
        return render(request, 'accounts/ModifierCommande.html', contex )
    

    # partie  pour modifier

    if request.method == "POST":
        client = Client.objects.get(pk=Client.id)
        Commande.Nom = request.POST.get("Nom")
        Commande.Telephone = request.POST.get("Telephone")
        #Client = request.POST.get("Client")
        Commande.Modele_Couture = request.POST.get("Modele_Couture")
        Commande.Nombre_Pagnes = request.POST.get("Nombre_Pagnes")
        Commande.Dos = request.POST.get("Dos")
        Commande.Epaule = request.POST.get("Epaule")
        Commande.Poitrine = request.POST.get("Poitrine")
        Commande.Longueur_Manche = request.POST.get("Longueur_Manche")
        Commande.Tour_Manche = request.POST.get("Tour_Manche")
        Commande.Longueur_Taille = request.POST.get("Longueur_Taille")
        Commande.Tour_Taille = request.POST.get("Tour_Taille")
        Commande.Pince_longueur_seins = request.POST.get("Pince_longueur_seins")
        Commande.Longueur_Camisole = request.POST.get("Longueur_Camisole")
        Commande.Longueur_Robe = request.POST.get("Longueur_Robe")
        Commande.Longueur_Chemise = request.POST.get("Longueur_Chemise")
        Commande.Messure_Bassin = request.POST.get("Messure_Bassin")
        Commande.Mesure_Ceinture = request.POST.get("Mesure_Ceinture")
        Commande.Mesure_Cuisse = request.POST.get("Mesure_Cuisse")
        Commande.Mesure_Genoux = request.POST.get("Mesure_Genoux")
        Commande.Longeur_Jupe = request.POST.get("Longeur_Jupe")
        Commande.Longueur_Bras = request.POST.get("Longueur_Bras")
        Commande.Longueur_Poignet = request.POST.get("Longueur_Poignet")
        Commande.Prix_Couture = request.POST.get("Prix_Couture")
        Commande.Avance = request.POST.get("Avance")
        Commande.Date_Depot_Model = request.POST.get("Date_Depot_Model")
        Commande.Date_Retrait_Model = request.POST.get("Date_Retrait_Model")
       
        Commande.objects.create(
                                            client=client,
                                            Modele_Couture=Commande.Modele_Couture,
                                            Nombre_Pagnes=Commande.Nombre_Pagnes, 
                                            Dos=Commande.Dos, 
                                            Epaule=Commande.Epaule, 
                                            Poitrine=Commande.Poitrine, 
                                            Longueur_Manche=Commande.Longueur_Manche, 
                                            Tour_Manche=Commande.Tour_Manche ,
                                            Longueur_Taille=Commande.Longueur_Taille,
                                            Tour_Taille=Commande.Tour_Taille, 
                                            Pince_longueur_seins=Commande.Pince_longueur_seins, 
                                            Longueur_Camisole=Commande.Longueur_Camisole, 
                                            Longueur_Robe=Commande.Longueur_Robe, 
                                            Longueur_Chemise=Commande.Longueur_Chemise, 
                                            Messure_Bassin=Commande.Messure_Bassin, 
                                            Mesure_Ceinture=Commande.Mesure_Ceinture, 
                                            Mesure_Cuisse=Commande.Mesure_Cuisse, 
                                            Mesure_Genoux=Commande.Mesure_Genoux, 
                                            Longeur_Jupe=Commande.Longeur_Jupe, 
                                            Longueur_Bras=Commande.Longueur_Bras, 
                                            Longueur_Poignet=Commande.Longueur_Poignet, 
                                            Prix_Couture=Commande.Prix_Couture, 
                                            Avance=Commande.Avance, 
                                            Date_Depot_Model=Commande.Date_Depot_Model, 
                                            Date_Retrait_Model=Commande.Date_Retrait_Model).save()
        commande.save()
        messages.success(request, "Commande modifiee avec succes")
        return redirect('accounts:liste_commande')
    
    return render(request, "accounts/ModifierCommande.html")

# Suppression d'une commande

def supprimer_commande(request, commande_id):
    commande = Commande.objects.get(pk = commande_id)
    #client = commande.Client
    
    commande.delete()
    #Client.Interventions -=1
    #client.save()
    messages.success(request, "Cette commande a ete bien supprimee")
    return redirect('accounts:liste_commande')


# Facture

'''def facture(request, facture_id):
   # client = Client.objects.get(pk = facture_id)
    facture = Facture.objects.get(pk = facture_id)
    contexte = {
        #'client' : client,
        'facture':facture
    }
    return render(request, 'accounts/Facture.html', contexte)'''


'''def commandes_de_chaque_client(request, Telephone):
    try:
        commandes = Commande.objects.all(pk=Telephone)
        client = Client.objects.get(Telephone=Telephone)
    #    commandes= Commande.objects.filter(client=client)
        context ={
            'client': client,
            'commandes': commandes

        }

        return render(request, "accounts/Commandes_de_chaque_client.html", context)
    except Client.DoesNotExist:
        return redirect('accounts:client')'''
    
def profil(request, profil_id):
    if request.method == "GET":
        #commandes = Commande.objects.all()
        #clients = Client.objects.get(pk=profil_id)
        clients = Client.objects.filter(pk=profil_id)
        commandes = Commande.objects.filter(Telephone=profil_id)
        context ={  'clients': clients, 'commandes': commandes }
        return render (request, "accounts/Commandes_de_chaque_client.html", context=context)
    
def facture(request, facture_id):
    if request.method == "GET":
        #commandes = Commande.objects.all()
        #clients = Client.objects.get(pk=profil_id)
        clients = Client.objects.filter(pk=facture_id)
        commandes = Commande.objects.filter(pk=facture_id)
        factures = Facture.objects.filter(Telephone=facture_id)

        context ={  'clients': clients, 'factures': factures , "commandes": commandes}
        #clients = Client.objects.all()
        #factures = []
        #for client in clients:
            #factures.append

        return render (request, "accounts/Facture.html", context=context)