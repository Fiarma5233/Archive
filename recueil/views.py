from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from Archive import settings
from django.contrib.auth.models import User  # Pour la creation d'utilisateurs
from django.contrib.auth import authenticate, login, logout # Pour conexion, deconnexion et authentification
from django.contrib.auth.decorators import login_required
#from Couture import settings  # Pour avoir acces elements pour l'envoi du mail se trouvant dans settings
from django.core.mail import send_mail, EmailMessage  # Pour l'envoi du mail
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from .token import generatorToken # importation de l'instance de classe TokenGenerator depuis le fichier token.py
from django.contrib import messages # Pour generer les messages d'erreur ou de succes
from django.views.decorators.csrf import csrf_exempt




# Create your views here.










#####################################################################################
####################################################################################
####################################################################################







@csrf_exempt
def inscription(request):
    if request.method =="GET":

        contexte = {
            "titre1": "Inscription",
            "message" : "Bonsoir",
            }
        return render (request, "recueil/Inscription.html")
    
    
    if request.method == 'POST':
    # Recuperation des donnees entrees par l'utilisateur
        lastname = request.POST.get('lastname')
       
        firstname = request.POST.get('firstname')
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password1 = request.POST.get("password1")

        if lastname == "":
            #messages.error(request, "Veuillez remplir ce champ")
            erreur1 = "Veuillez remplir ce champ"
            return render(request, "recueil/Inscription.html", context={"erreur1": erreur1})

        if firstname == "":
            #messages.error(request, "Veuillez remplir ce champ")
            erreur2 = "Veuillez remplir ce champ"
            return render(request, "recueil/Inscription.html", context={"erreur2": erreur2})

        if User.username == "":
            #messages.error(request, "Veuillez remplir ce champ")
            erreur3 = "Veuillez remplir ce champ"
            return render(request, "recueil/Inscription.html", context={"erreur3": erreur3})

        if User.objects.filter(username=username):
            #messages.error(request, "Ce nom existe deja")
            #return redirect("inscription")
            erreur3 = "Ce compte existe deja"
            return render(request, "recueil/Inscription.html", context={"erreur3": erreur3})

        
        if User.objects.filter(email=email):
            #messages.error(request, "Cet email a deja un compte")
            # return redirect("inscription")
            erreur4 = "Cet email a deja un compte"
            return render(request, "recueil/Inscription.html", context={"erreur4": erreur4})

        if password == '':
            erreur5 = "Veuillez remplir ce champ!"
            return render(request, "recueil/Inscription.html", context={"erreur5": erreur5})

        if password != password1 :
            #messages.error(request, "Les deux mots de passe doivent etre les memes")
            #return redirect("inscription")
            erreur6 = 'Les deux mots de passe doivent etre les memes'
            return render(request, "recueil/Inscription.html", context={"erreur6": erreur6})

        #couturier = Couturier.objects.create(Lastname=Lastname ,  Firstname=Firstname, Company=Company, Email=Email, Password=Password, PasswordConfirm=PasswordConfirm )                   # Appel de notre model
        couturier = User.objects.create_user( username, email, password )                   # Appel de notre model
        couturier.first_name = firstname
        couturier.last_name = lastname
        #couturier.password= Password

        couturier.is_active = False # Utilisateur non active
        couturier.save() # Enregistrement de nos donnees dans la db
        #messages.success(request, 'Votre compte a ete creee avec succes')

        #   Email de Bienvenue
        '''subject = "Soyez la bienvenue a l'entreprise "  + username + '!!!'     # Sujet de notre mail
        message = "Bienvenu " + couturier.first_name + " " + couturier.last_name + "\n\n\n Fiarma SOME"  #Message a envoyer
        form_email = settings.EMAIL_HOST_USER  # Adrresse mail qui va envoyer le mail
        to_list = [couturier.email]  # Destinataire du mail
        send_mail(subject, message, form_email, to_list, fail_silently=False) # Envoi du mail'''

        # Email de confirmation
        current_site = get_current_site(request)  # Pour avoir le lien du site
        email_subject = "Inscription de " + couturier.username  # Sujet du mail

           # email_subject = " Renitialisation de mot de passe de "  + couturier.username  # Sujet du mail

        '''messageConfirm = render_to_string("emailConfirm.html", {
            "name" : couturier.first_name,  # Prenom de l'utilisateur
            "domain": current_site.domain,  # Nom du domaine (site)
            "uid" :urlsafe_base64_encode(force_bytes(couturier.pk)), # Donner un id chaque lien endode sur64 bits
            "token": generatorToken.make_token(couturier)
        }) # Confirmation du message dans un fichier'''

        messageConfirm = f"Salut {couturier.first_name} {couturier.last_name} !!! \n\n\n Vous  venez de vous inscrire. Vous pouvez desormais vous connecter avec vos identifiants. \n Pour cela, veuillez cliquer sur le lien ci-dessous !!! \n\n Lien : {request.scheme}://{request.get_host()}/ \n\n Fiarma Landry SOME"


        # Pour envoi
        email = EmailMessage(
            email_subject,
            messageConfirm,
            settings.EMAIL_HOST_USER,
            [couturier.email]
        )

        email.fail_silently = False  #  Ceci permet d'indiquer les eventuelles erreurs liees a l'envoi du mail
        email.send() # Envoi




        return render(request, 'recueil/verification.html')

                             
    return render(request, "recueil/Inscription.html", contexte)

'''def activate(request, uidb64, token): # cette fonction genere le lien de confimation unique a chaque utilisateur
    try:
        # Verifions si le lien correspond a l'utilisateur en question
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and generatorToken.check_token(user, token):
        user.is_active = True  # C'est lorsqu'on clique sur le lien de confirmation que l'utilisateur est actif
        user.save() # On l'enrregistre
        messages.success(request, "Congratulations !!! Votre compte a ete activated")
        return redirect("connexion")
    
    else:
        messages.error(request, "Echec d'activation de votre compte. Reessayer plutard !!!")
        return redirect("connexion")'''


def connexion(request):
    '''if request.method == "GET":
        couturier = Couturier.objects.all()
        return render (request, "accounts/Connexion.html", {"couturier" : couturier})'''
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST["password"]
        # verification avec la methode 
        user = authenticate(username=username, password=password)
        try:
            my_user = User.objects.get(username=username)
            '''if username != username or password != password:
                erreur = "Vos identifiants sont incorrects"
                return render(request, 'accounts/Connexion.html', context={'erreur':erreur})'''

        except User.DoesNotExist:
            #messages.error(request, "Ce compte n'existe pas")
            erreur = "Ce compte n'existe pas"
            return render(request, 'recueil/Connexion.html', context={'erreur':erreur})
        
        # Verifions si l'utilisateur existe 
        if user is not None:
            login(request, user)
            firstname = user.first_name
            return  render(request, "recueil/universityList.html", {"firstname" : firstname}) #render(request, "accounts/Home.html", {"firstname" : firstname})
        
        #elif my_user.username.DoesNotExist:
            
        
        elif my_user.is_active == False:  # Si l'utilisateur tente de se connecter sans avoir confirmer  son addresse
            #messages.error(request, "Vous n'avez pas encore confirme votre addresse email. Faites-le avant de vous connecter !!!")
            erreur = "Confirmez d'abord votre adresse email !"
            return render(request, 'recueil/Connexion.html', context={'erreur':erreur})


        else:
            #messages.error(request, "Mauvaise authentification")
            erreur = "Mauvaise authentification"
            return render(request, 'recueil/Connexion.html', context={'erreur':erreur})
            #return redirect('connexion')
        
       

    return render(request, 'recueil/Connexion.html')


@login_required
def deconnexion(request):
    logout(request)
    messages.success(request, "Vous avez ete deconnecte")
    return redirect("connexion")



def renitialiser(request):

   
    if request.method =="GET":
        #users = User.objects.all()
        #users = User.objects.filter(email=User.email)    # On get l'utilisateur ayant cet email
        return render(request, "recueil/renitialiser.html" )
    
    #users = User.objects.all()
    #users = User.objects.filter(email=User.email)
    #User.is_activate = True

    #User.objects.get(email=email).is_active = True
    if request.method == "POST":
        email = request.POST.get('email') #On requpere la valeur de l'adrresse email
        
        couturier = User.objects.filter(email=email).first()
        if couturier : # On verivie si cet email correspond pas vraiement a celui de l'user
            #erreur = "Cette addresse email n'existe pas" #On resourne une esseur
            #return render(request, "accounts/renitialiser.html", context={"erreur": erreur} )
        
            #   Email de Bienvenue
            '''subject = " Renitialisation de mot de passe de "  + couturier.username + '!!!'     # Sujet de notre mail
            message = "Ne vous inquietez pas " + couturier.first_name + " " + couturier.last_name + " Vous allez bientot renitialiser votre mot de passe " +  " \n\n\n Fiarma SOME"  #Message a envoyer
            form_email = settings.EMAIL_HOST_USER  # Adrresse mail qui va envoyer le mail
            to_list = [couturier.email]  # Destinataire du mail
            send_mail(subject, message, form_email, to_list, fail_silently=False) # Envoi du mail'''

            # Email de renitialisation
            current_site = get_current_site(request)  # Pour avoir le lien du site
            email_subject = " Renitialisation de mot de passe de "  + couturier.username  # Sujet du mail
            """
            messageConfirm = render_to_string("confirmerRenitialisation.html", {
                "name" : couturier.first_name,  # Prenom de l'utilisateur
                "domain": current_site.domain,  # Nom du domaine (site)
                "uid" :urlsafe_base64_encode(force_bytes(couturier.pk)), # Donner un id chaque lien endode sur64 bits
                "token": generatorToken.make_token(couturier)
            }) # Confirmation du message dans un fichier
            """
            
            messageConfirm = f"Salut {couturier.first_name} {couturier.last_name} !!! \n\n\n Vous avez oublie votre mot de passe et vous souhaitez le renitialliser. \n Pour cela, veuillez cliquer sur le lien ci-dessous !!! \n\n Lien : {request.scheme}://{request.get_host()}/nouveauPasse/{urlsafe_base64_encode(force_bytes(couturier.pk))}/{generatorToken.make_token(couturier)} \n\n Fiarma Landry SOME"

            # Pour envoi
            email = EmailMessage(
                email_subject,
                messageConfirm,
                settings.EMAIL_HOST_USER,
                [couturier.email]
            )

            email.fail_silently = False  #  Ceci permet d'indiquer les eventuelles erreurs liees a l'envoi du mail
            email.send() # Envoi
            return render(request, "recueil/verification.html")

        else:
            erreur = "Cette adresse email n'existe pas"
            return render(request, "recueil/renitialiser.html", context={"erreur":erreur} )

    return render(request, "recueil/renitialiser.html" )



"""
def Confirmeration(request, uidb64, token): # cette fonction genere le lien de confimation unique a chaque utilisateur
    print(uidb64, token)
    try:
        # Verifions si le lien correspond a l'utilisateur en question
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and generatorToken.check_token(user, token):
        user.is_active = True  # C'est lorsqu'on clique sur le lien de confirmation que l'utilisateur est actif
        user.save() # On l'enrregistre
        messages.success(request, "Congratulations !!! Votre compte a ete activated")
        #return render(request, "accounts/verification.html")
        return render(request, 'accounts/nouveauPasse.html')
    
    else:
        messages.error(request, "Echec d'activation de votre compte. Reessayer plutard !!!")
        return render(request, "accounts/verification.html")

"""

def nouveauPasse(request, uidb64, token):
    #users = User.objects.all()
    #users = User.objects.filter(email=User.email)
    #User.is_activate = True
    #user = None
    
    #token = Confirmeration.token
    #if request.method =="GET":
        #couturier = User.objects.all()
        #couturier = User.objects.filter(email=User.email)    # On get l'utilisateur ayant cet email
        #return render(request, "accounts/renitialiser.html")
        #User.is_activate = True

    #User.is_activate = True
   # utilisateur = User.objects.all()
    #email = User.email
    #couturier = User.objects.all()
    #users = User.objects.filter(email=email)

    #user = User.objects.get(email=User.email) 

    if request.method == "POST":
        

        password = request.POST.get("password")
        password1 = request.POST.get('password1')

        uid_pk = force_text(urlsafe_base64_decode(uidb64))

        #Couturier = User.objects.filter(pk=uid_pk).first()
        Couturier = User.objects.get(pk=uid_pk)

        print(f"Les nouveaux passes sont:\t\t {password} \t et \t {password1}")
        if password == '':
            erreur1 = "Le mot de passe ne doit pas etre vide"
            return render(request, "recueil/nouveauPasse.html", context={"erreur1": erreur1})
        
        '''if len(password) < 8 or len(password) >10:
            erreur1 = "Le mot de passe ne doit contenir au plus 10 caracteres"
            return render(request, "accounts/nouveauPasse.html", context={"erreur1": erreur1})'''

        if password != password1 :
            erreur2 = "Les mots de passe doivent etre les memes"
            return render(request, "recueil/nouveauPasse.html", context={"erreur2": erreur2})
        
        #couturier = User.objects.get(email=email) 

        #password = int(password)
        #password1 = int(password1)

        #User.password = password
        #User.password.save()
       # users= User.password
        #users.save()

        is_valid = generatorToken.check_token(Couturier, token)
        if is_valid:
            Couturier.set_password(password)
            Couturier.is_active=True
            Couturier.save()

            #Couturier = User.objects.get(email=email) 
            '''subject = " Vous venez de renitialiser votre mot de passe "    # Sujet de notre mail
            #message =  f"{User.first_name } {User.last_name} Votre nouveau mot de passe est : \t\t  + {User.password } \n\n\n Fiarma SOME"  #Message a envoyer
            #message =  User.first_name + User.last_name +  " Votre nouveau mot de passe est : \t\t " + User.password + " \n\n\n Fiarma SOME"  #Message a envoyer
            message =    " Votre nouveau mot de passe est : \t\t " + Couturier.password + " \n\n\n Fiarma SOME"  #Message a envoyer

            form_email = settings.EMAIL_HOST_USER  # Adrresse mail qui va envoyer le mail
            to_list = [Couturier.email]  # Destinataire du mail
            send_mail(subject, message, form_email, to_list, fail_silently=False) # Envoi du mail
            print(f"Mon adresse mail est :\t\t {User.email}")'''

            # Email de renitialisation
            current_site = get_current_site(request)  # Pour avoir le lien du site
            email_subject = "Nouveau mot de passe"
            #email_subject = f" Vous venez de renitiaaliser votre mot de  passe  qui est desormais {Couturier.password} "   #User.username + "  Connectez desormais avec votre nouveau  mot de passe de "  # Sujet du mail

            #messageConfirm = f"Vous venez de renitialiser votre mot de  passe  qui est desormais {Couturier.password} \n \n Veuillez cliquer sur le lien ci-dessous pour se connecter !!! \n\n Lien : {request.scheme}://{request.get_host()}/connexion/{urlsafe_base64_encode(force_bytes(Couturier.pk))}/{generatorToken.make_token(Couturier)} \n\n Fiarma Landry SOME"
            messageConfirm = f"Vous venez de renitialiser votre mot de  passe  qui est desormais {Couturier.password} \n \n Veuillez cliquer sur le lien ci-dessous pour se connecter !!! \n\n Lien : {request.scheme}://{request.get_host()}/ \n\n Fiarma Landry SOME"

            '''messageConfirm = render_to_string("finPasse.html", {
                "name" : Couturier.first_name,  # Prenom de l'utilisateur
                "domain": current_site.domain,  # Nom du domaine (site)
                "uid" :urlsafe_base64_encode(force_bytes(Couturier.pk)), # Donner un id chaque lien endode sur64 bits
                "token": generatorToken.make_token(Couturier)
            }) # Confirmation du message dans un fichier'''

            # Pour envoi
            email = EmailMessage(
                email_subject,
                messageConfirm,
                settings.EMAIL_HOST_USER,
                [Couturier.email]
            )

            email.fail_silently = False  #  Ceci permet d'indiquer les eventuelles erreurs liees a l'envoi du mail
            email.send() # Envoi

            print(Couturier.email)
            return render(request, 'recueil/verification.html')


    return render(request, "recueil/nouveauPasse.html")





'''def fin(request, uidb64, token): # cette fonction genere le lien de confimation unique a chaque utilisateur
    try:
        # Verifions si le lien correspond a l'utilisateur en question
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and generatorToken.check_token(user, token):
        user.is_active = True  # C'est lorsqu'on clique sur le lien de confirmation que l'utilisateur est actif
        user.save() # On l'enrregistre
        messages.success(request, "Congratulations !!! Votre compte a ete activated")
        #succes = "Vous ave"
        return redirect("connexion")
    
    else:
        messages.error(request, "Echec d'activation de votre compte. Reessayer plutard !!!")
        return redirect("connexion")'''










####################################################################################
####################################################################################
###################################################################################













#Vue pour ajouter une universite
def university(request):

    if request.method == "POST":
        nom = request.POST.get('nom')
        photo = request.FILES.get('photo')

        university = University.objects.create(
            nom=nom,
            photo=photo
        )

        if nom == '':
            ereur1 = 'Ce champ ne doit pas etre vide !!!'
            return render(request, 'recueil/university.html', {'ereur1': ereur1})

        if photo == '':
            ereur2 = 'Ce champ ne doit pas etre vide !!!'
            return render(request, 'recueil/university.html', {'ereur2': ereur2})

        university.save()
        return redirect('recueil:universityList')
    return render(request, 'recueil/university.html')


# Vue pour afficher la liste des universites
def universityList(request):
    if request.method == 'GET':
        universities = University.objects.all()
        return render(request, 'recueil/universityList.html', {"universities":universities} )
    


def modifierUniversity(request, university_id):
    university = University.objects.get(id=university_id)

    if request.method == "POST":
        
        nom = request.POST.get('nom')
        new_photo = request.FILES.get('photo')
        photo = request.FILES.get('photo')


           
        

        if nom == '':
            ereur1 = 'Ce champ ne doit pas etre vide !!!'
            return render(request, 'recueil/university.html', {'ereur1': ereur1})

        if new_photo == '':
            ereur2 = 'Ce champ ne doit pas etre vide !!!'
            return render(request, 'recueil/university.html', {'ereur2': ereur2})


        university.nom=nom

        if new_photo:

            university.photo = new_photo
        
        university.save()

 
        return redirect('recueil:universityList')
    return render(request, 'recueil/modifierUniversity.html', {"university":university})



# Vue pour supprimer une universite
def supprimerUniversity(request, university_id):
    university =University.objects.get(id=university_id)
    university.delete()
    return redirect('recueil:universityList')


def ufr_par_university(request, university_id):
    university = University.objects.get(id=university_id)
    ufrs = UFR.objects.filter(university=university)
    return render(request, 'recueil/ufr_par_university.html', {"university":university, "ufrs":ufrs})
    


#Vue pour enregistrer une  ufr
def ufr(request):
    universities = University.objects.all()
    ufrs = []  # Liste vide pour les UFR, sera remplie plus tard


    if request.method == "POST":

        university_id = request.POST.get('university')

        # Vérifiez si une université a été sélectionnée
        if university_id is not None and university_id != '':
            try:
                university = University.objects.get(id=university_id)
            except University.DoesNotExist:
                erreur1 = 'L\'université sélectionnée n\'existe pas.'
                return render(request, 'recueil/ufr.html', {'erreur1': erreur1})
        else:
            erreur1 = 'Veuillez sélectionner une université.'
            return render(request, 'recueil/ufr.html', {'erreur1': erreur1})



       
        nom =request.POST.get('nom')

        if nom == '':
            ereur2 = 'Ce champ ne doit pas etre vide !!!'
            return render(request, 'recueil/ufr.html', {'ereur2': ereur2})
        
        # Filtrer les UFR en fonction de l'université sélectionnée
        ufrs = UFR.objects.filter(university=university)


        ufr = UFR.objects.create(
            university=university,
            nom=nom
        )

        ufr.save()

        return redirect('recueil:ufrList')
    return render(request, 'recueil/ufr.html', {'universities':universities,'ufrs': ufrs})


# Vue pour afficher la liste des ufr
def ufrList(request):
    if request.method == "GET":
        ufrs = UFR.objects.all()
        return render(request, 'recueil/ufrList.html', {'ufrs':ufrs})
    

#Vue pour modifier  une ufr
def modifierUfr(request, ufr_id):
    universities = University.objects.all()
    ufr = UFR.objects.get(id = ufr_id)

    if request.method == "POST":
        university_id = request.POST.get('university')
        university = University.objects.get(id=university_id)

        nom = request.POST.get('nom')
        if nom == '':
            ereur1 = 'Ce champ ne doit pas etre vide !!!'
            return render(request, 'recueil/modifierUfr.html', {'ereur1': ereur1})


        ufr.university=university
        ufr.nom = nom

        ufr.save()

        return redirect('recueil:ufrList')
    return render(request, 'recueil/modifierUfr.html', {"universities":universities, 'ufr':ufr})

# Vue pour supprimer une ufr
def supprimerUfr(request, ufr_id):
    ufr = UFR.objects.get(id=ufr_id)
    ufr.delete()
    return redirect('recueil:ufrList')





def filiere_par_ufr(request, ufr_id):
    ufr = UFR.objects.get(id=ufr_id)
    filieres = Filiere.objects.filter(ufr=ufr)
    return render(request, 'recueil/filiere_par_ufr.html', {"ufr":ufr, "filieres":filieres})

    


# Vue pour creeer ou ajouter une filiere
def filiere(request):
    universities = University.objects.all()
    ufrs = UFR.objects.all()

    if request.method =="POST":

        ufr_id = request.POST.get('ufr')
        ufr = UFR.objects.get(id=ufr_id)

        nom = request.POST.get('nom')
        if nom == '':
            ereur1 = 'Ce champ ne doit pas etre vide !!!'
            return render(request, 'recueil/filiere.html', {'ereur1': ereur1})
        
        
        filiere = Filiere.objects.create(
            ufr=ufr,
            nom=nom
        )

        filiere.save()

        return redirect('recueil:filiereList')
    return render(request, 'recueil/filiere.html', { "universities": universities,"ufrs":ufrs})


# Vue pour afficher la liste des filieres
def filiereList(request):
    if request.method == "GET":
        filieres = Filiere.objects.all()
        return render(request, 'recueil/filiereList.html', {"filieres":filieres})
    
# Vue pour modifier une filiere
def modifierFiliere(request, filiere_id):
    ufrs = UFR.objects.all()
    filiere = Filiere.objects.get(id = filiere_id)

    if request.method == "POST":
        urf_id = request.POST.get('ufr')
        ufr = UFR.objects.get(id = urf_id)
        nom = request.POST.get('nom')
        
        if nom == '':
            ereur1 = 'Ce champ ne doit pas etre vide !!!'
            return render(request, 'recueil/modifierFiliere.html', {'ereur1': ereur1})
        
        filiere.ufr = ufr
        filiere.nom = nom
        filiere.save()

        return redirect('recueil:filiereList')
    return render(request, 'recueil/modifierFiliere.html', {"ufrs":ufrs, "filiere":filiere})

# Vue pour supprimer une  filiere
def supprimerFiliere(request, filiere_id):
    filiere = Filiere.objects.get(id=filiere_id)
    filiere.delete()
    return redirect('recueil:filiereList')

def niveau_par_filiere(request, filiere_id):
    filiere = Filiere.objects.get(id = filiere_id)
    niveaux = Year.objects.filter(filiere=filiere)
    return render(request, 'recueil/niveau_par_filiere.html', {"filiere":filiere, "niveaux":niveaux})


        
        

def semeste_par_niveau(request, year_id):
    year = Year.objects.get(id = year_id)
    semestres = Semestre.objects.filter(year=year)
    return render(request, 'recueil/semeste_par_niveau.html', {"year":year, "semestres":semestres})


def adama (request):
    if request.method =="GET":
        return render (request, 'recueil/adama.html')


    















# Vue pour ajouter un annee

def year(request):
    filieres = Filiere.objects.all()
    if request.method == 'POST':
        filiere_id = request.POST.get('filiere')
        filiere = Filiere.objects.get(id=filiere_id)
        nom = request.POST.get('nom')
        periode = request.POST.get('periode')

        if nom == '':
            erreur1 = 'Ce champ ne doit pas etre vide'
            return render(request, 'recueil/year.html', {'erreur1':erreur1})

        if periode == '':
            erreur2 = 'Ce champ ne doit pas etre vide'
            return render(request, 'recueil/year.html', {'erreur2':erreur2})

        year = Year.objects.create(
            filiere=filiere,
            nom=nom,
            periode=periode
        )

        year.save()
    
    #return render(request, 'recueil:year.html')
        return redirect('recueil:yearList')
    return render(request, 'recueil/year.html', {"filieres":filieres})





# Vue pour afficher les annees
def yearList(request):
    if request.method == "GET":
        years = Year.objects.all()
    
    #return render(request, 'recueil/yearList.html', {'years': years})

    return render(request, 'recueil/yearList.html', {'years':years})


# vue pour modifier les annees
def modifierYear(request, year_id):
    filieres = Filiere.objects.all()
    year = Year.objects.get(id=year_id)
    if request.method == 'POST':
        filiere_id = request.POST.get('filiere')
        filiere = Filiere.objects.get(id=filiere_id)
        nom = request.POST.get('nom')
        periode = request.POST.get('periode')

        if nom == '':
            erreur1 = 'Ce champ ne doit pas etre vide'
            return render(request, 'recueil/modifierYear.html', {'erreur1':erreur1})

        if periode == '':
            erreur2 = 'Ce champ ne doit pas etre vide'
            return render(request, 'recueil/modifierYear.html', {'erreur2':erreur2})
        
        year.filiere =filiere
        year.nom = nom
        year.periode = periode

        year.save()
        return redirect('recueil:yearList')
    return render(request, 'recueil/modifierYear.html', {'year':year , "filieres":filieres})


# Vue pour supprimer
def supprimerYear(request, year_id):
    if request.method == "GET":
        year = Year.objects.get(id=year_id)
        year.delete()
        return redirect('recueil:yearList')
        #return redirect('recueil:moduleList')



# Vue pour ajouter un semestre
def semestre(request):
     
    years = Year.objects.all() # Pour avoir tous les niveaux
     
    if request.method == 'POST':

        year_id = request.POST.get('year') # on recupere l'id
        year = Year.objects.get(id=year_id)

        nom = request.POST.get('nom')
        #periode = request.POST.get('periode')

        if nom == '':
            erreur1 = 'Ce champ ne doit pas etre vide'
            return render(request, 'recueil/semestre.html', {'erreur1':erreur1})

        
        semestre = Semestre.objects.create(
            year=year,
            nom=nom
            
        )

        semestre.save()
    
    #return render(request, 'recueil:year.html')
        return redirect('recueil:semestreList')
    return render(request, 'recueil/semestre.html', {'years':years})

# Vue pour afficher les annees
def semestreList(request):
    if request.method == "GET":
        semestres = Semestre.objects.all()
    
    #return render(request, 'recueil/yearList.html', {'years': years})

    return render(request, 'recueil/semestreList.html', {'semestres':semestres})


# Vue pour modifier un semestre
def modfifierSemestre(request, semestre_id):

    years = Year.objects.all()
    semestre = Semestre.objects.get(id=semestre_id)

    if request.method == "POST":
        year_id = request.POST.get('year') # on recupere l'id
        year = Year.objects.get(id=year_id)

        nom = request.POST.get('nom')
        #periode = request.POST.get('periode')

        if nom == '':
            erreur1 = 'Ce champ ne doit pas etre vide'
            return render(request, 'recueil/modifierSemestre.html', {'erreur1':erreur1})

        semestre.year = year 
        semestre.nom = nom
        semestre.save()
        return redirect('recueil:semestreList')

    
    return render(request, 'recueil/modifierSemestre.html', {'years':years, 'semestre':semestre})

#Vue pour supprimer un semestre
def supprimerSemestre(request, semestre_id):
    semestre = Semestre.objects.get(id=semestre_id)
    semestre.delete()
    return redirect('recueil:semestreList')



# Vue pour ajouter un semestre
def module(request):
     
    semestres = Semestre.objects.all() # Pour avoir tous les niveaux
     
    if request.method == 'POST':

        semestre_id = request.POST.get('semestre') # on recupere l'id
        semestre = Semestre.objects.get(id=semestre_id) # on fait de ca la cle etrangere

        nom = request.POST.get('nom')
        #periode = request.POST.get('periode')

        if nom == '':
            erreur1 = 'Ce champ ne doit pas etre vide'
            return render(request, 'recueil/module.html', {'erreur1':erreur1})

        
        module = Module.objects.create(
            semestre=semestre,
            nom=nom
            
        )

        module.save()
    
    #return render(request, 'recueil:year.html')
        return redirect('recueil:moduleList')
    return render(request, 'recueil/module.html', {'semestres':semestres})




# Vue pour afficher les modules
def moduleList(request):
    if request.method == "GET":
        modules = Module.objects.all()
    
    #return render(request, 'recueil/yearList.html', {'years': years})

    return render(request, 'recueil/moduleList.html', {'modules':modules})


# Vue pour modifier un semestre
def modifierModule(request, module_id):

    semestres = Semestre.objects.all()
    module = Module.objects.get(id=module_id)

    if request.method == "POST":
        semestre_id = request.POST.get('semestre') # on recupere l'id
        semestre = Semestre.objects.get(id=semestre_id)

        nom = request.POST.get('nom')
        #periode = request.POST.get('periode')

        if nom == '':
            erreur1 = 'Ce champ ne doit pas etre vide'
            return render(request, 'recueil/modifierModule.html', {'erreur1':erreur1})

        module.semestre = semestre 
        module.nom = nom
        module.save()
        return redirect('recueil:moduleList')

    
    return render(request, 'recueil/modifierModule.html', {'semestres':semestres, 'module':module})

#Vue pour supprimer un semestre
def supprimerModule(request, module_id):
    module = Module.objects.get(id = module_id)
    module.delete()
    return redirect('recueil:semestreList')



###############################################




# Vue pour ajouter un semestre
def fichier(request):
     
    modules = Module.objects.all() # Pour avoir tous les niveaux
     
    if request.method == 'POST':

        module_id = request.POST.get('module') # on recupere l'id
        module = Module.objects.get(id=module_id)

        file =request.FILES.get('file')

        #nom = request.POST.get('nom')

        status = request.POST.get('status')

        if  file == '':
            erreur1 = 'Ce champ ne doit pas etre vide'
            return render(request, 'recueil/fichier.html', {'erreur1':erreur1})


        
        
        fichier = Fichier.objects.create(
            module=module,
            file=file,
            status=status
            
        )

        fichier.save()
    
    #return render(request, 'recueil:year.html')
        return redirect('recueil:fichierList')
    return render(request, 'recueil/fichier.html', {'modules':modules})




# Vue pour afficher les modules
def fichierList(request):
    if request.method == "GET":
        fichiers = Fichier.objects.all()
    
    #return render(request, 'recueil/yearList.html', {'years': years})

    return render(request, 'recueil/fichierList.html', {'fichiers':fichiers})


# Vue pour modifier un semestre
def modifierFichier(request, fichier_id):

    modules = Module.objects.all()
    fichier = Fichier.objects.get(id=fichier_id)

    if request.method == "POST":
        module_id = request.POST.get('module') # on recupere l'id
        module = Module.objects.get(id=module_id)

        #file =request.FILES.get('file')

        new_file = request.FILES.get('file')  # Nouveau fichier téléchargée



        status = request.POST.get('status')


        '''if  file == '':
            erreur1 = 'Ce champ ne doit pas etre vide'
            return render(request, 'recueil/modifierFichier.html', {'erreur1':erreur1})'''


       
        fichier.module = module
        if new_file:
            fichier.file = new_file
        #fichier.file = file
        fichier.status =status
        fichier.save()
        return redirect('recueil:fichierList')

    
    return render(request, 'recueil/modifierFichier.html', {'modules':modules, 'fichier':fichier})

#Vue pour supprimer un semestre
def supprimerFichier(request, fichier_id):
    fichier = Fichier.objects.get(id = fichier_id)
    fichier.delete()
    return redirect('recueil:fichierList')


# Vue pour afficher les semestres par niveau
def semeste_par_niveau(request, year_id):
    year = get_object_or_404(Year, id=year_id)
    semestres = Semestre.objects.filter(year=year)
    return render(request, 'recueil/semeste_par_niveau.html', {'semestres': semestres, 'year':year})


# Vue pour afficher les modules par semestres
def module_par_semestre(request, semestre_id):
    semestre = get_object_or_404(Semestre, id=semestre_id)
    modules = Module.objects.filter(semestre=semestre)
    return render(request, 'recueil/module_par_semestre.html', {'semestre': semestre, 'modules':modules})

# Vue pour affichier les cours par modules
def cours_par_modules(request, module_id):
    module = get_object_or_404(Module, id = module_id)

    fichiers =  Fichier.objects.filter(module=module)
    '''courses = Fichier.status =='Cours'
    TP = Fichier.status =="TP"
    Autres = Fichier.status =="Autres" '''

    return render(request, 'recueil/cours_par_modules.html', {'fichiers':fichiers, 'module':module, })



