from django.db import models
import os


# Create your models here.

class University(models.Model):
    nom =models.CharField(max_length=200, null=False, blank=False)
    photo = models.ImageField(upload_to='recueil', blank=False, null=False)
    date = models.DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return self.nom
    
    @property
    def photoUrl(self):
        try:
            url = self.photo.url
        except ValueError:
            url = ''
        return url
    

class UFR(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    nom = models.CharField(max_length=200, null=False, blank=False)
    date = models.DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return self.nom
    
    
class Filiere(models.Model):
    #university = models.ForeignKey(University, on_delete=models.CASCADE)

    ufr = models.ForeignKey(UFR, on_delete=models.CASCADE)
    nom = models.CharField(max_length=200, null=False, blank=False)
    date = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.nom
    

class Year(models.Model):
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE)

    #filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE)
    nom = models.CharField(max_length=200, blank=False, null=False)
    periode = models.CharField(max_length=200, blank=False, null=False)
    date = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.nom
    
class Semestre(models.Model):
    year = models.ForeignKey(Year, on_delete=models.CASCADE)
    nom = models.CharField(max_length=200, blank=False)
    date = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.nom
    

class Module(models.Model):
    semestre = models.ForeignKey(Semestre, on_delete=models.CASCADE)
    nom = models.CharField(max_length=200, blank=False)
    date = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.nom



class Fichier(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    file = models.FileField(upload_to='recueil', blank=False, null=False)
   # nom = models.CharField(max_length=200, blank=False)
        
    CHOIX = [
        ('Cours', 'Cours'),
        ('TD', 'TD'),
        ('Autres', 'Autres')
    ]
    
    status = models.CharField(
        max_length=50,
        choices=CHOIX,
        default='Cours'
    )
    date = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.nom
    
    '''
        Cette propriete permet d'afficher seulement les noms des fichiers
            df
        '''
    @property  
   
    def get_file_name(self):
        return os.path.basename(self.file.name)
    
    
    # autorisation d'afficher un produit sans image
    @property
    def fileUrl(self):
        try:
            url = self.file.url
        except ValueError:
            url = ''
        return url
    
    


