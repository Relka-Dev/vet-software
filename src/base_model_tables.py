from django.db import models

class Person(models.Model):
    first_name = models.CharField(
        max_length=100,
        verbose_name="Prénom"
    )
    last_name = models.CharField(
        max_length=100,
        verbose_name="Nom"
    )
    phone = models.IntegerField(
        verbose_name = "numéro de téléphone"
    )
    email = models.CharField(
        max_length=255
    )
    birthday = models.DateField()
    
    password_hash = models.CharField
    
    creation_date = models.DateField
    
    class Meta:
        verbose_name = "Personne"
        verbose_name_plural = "Personnes"
        
    def __str__(self):
        return f"Prénom:{self.first_name} Nom:{self.last_name} Téléphone:{self.phone}"
    
class Family(models.Model):
    main_contact_id = models.ForeignKey(
        Person,
        on_delete=models.PROTECT,
        #related_name="personne",
        verbose_name="contact principal"
    )
    creation_date = models.DateField()
    
    class Meta:
        verbose_name = "Famille"
        verbose_name_plural = "Familles"   
    
class Animal(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="nom de l'animal"
    )
    birthday = models.DateField
    
    federal_identification = models.IntegerField
    
    family_id = models.ForeignKey(
        Family,
        on_delete=models.PROTECT,
        #related_name="famille",
        verbose_name="identifiant famille"
    )
    
class Extra_family_member(models.Model):
    family_id = models.ForeignKey(
        Family,
        on_delete=models.PROTECT,
        #related_name="famille",
        verbose_name="identifiant famille"
    )
    person_id = models.ForeignKey(
        Person,
        on_delete=models.PROTECT,
        #related_name="personne",
        verbose_name="identifiant personne"
    )
    
class Role(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Fonction de l'employé"
    )
    
class Employee(models.Model):
    person_id = models.ForeignKey(
        Person,
        on_delete=models.PROTECT,
        #related_name="personne"
        verbose_name="identifiant personne"
    )
    first_engagement_date = models.DateField()
    
    role_id = models.ForeignKey(
        Role, 
        on_delete=models.PROTECT,
        #related_name="role"
        verbose_name="identifiant personne"
    )

class Room_type(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Type de salle"
    )

class Room(models.Model):
    room_type_id = models.ForeignKey(
        Room_type,
        verbose_name="Type de salle"
    )
    
class Emergency_type(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="type de rendez-vous"
    )
    
class Appointement(models.Model):
    animal_id = models.ForeignKey(
        Animal,
        verbose_name="identifiant aninmal"
    )
    room_id = models.ForeignKey(
        Room,
        verbose_name="identifiant salle"
    )
    employee_id = models.ForeignKey(
        Employee,
        verbose_name="identifiant employé"
    )
    emergency_type_id = models.ForeignKey(
        Emergency_type,
        verbose_name="identifiant type de rendez-vous"
    )
    start_date = models.DateTimeField
    end_date = models.DateTimeField
    
class Procedure(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Nom de la prodécure"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Prix (CHF)"
    )

class Appointement_procedure(models.Model):
    appointement_id = models.ForeignKey(
        Appointement,
        verbose_name="identifiant rendez-vous"
    )
    prodecure_id = models.ForeignKey(
        Procedure,
        verbose_name="identifiant procédure"
    )
    quantity = models.IntegerField()
    
class Disponibility_range(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    
class Disponibility_employee(models.Model):
    employee_id = models.ForeignKey(
        Employee,
        verbose_name="identifiant employé"
    )
    disponibility_range_id = models.ForeignKey(
        Disponibility_range,
        verbose_name="identifiant période"
    )