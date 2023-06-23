from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Books(models.Model):
    GENRE_CHOICES = [
        ('biografy', 'biografie'),
        ('child', 'dla dzieci'),
        ('horror', 'horror'),
        ('reportage', 'literatura faktu'),
        ('common_literature', 'literatura obyczajowa'),
        ('foreign_belles_lettres', ' literatura piękna obca'),
        ('polish_belles_lettres', 'literatura piękna polska'),
        ('romans', 'romans'),
        ('poezja', 'poezja'),
    ]

    language_choices = [
        ('english', 'angielski'),
        ('polish', 'polski')
    ]

    author = models.CharField(max_length=100,blank=True)
    title = models.CharField(max_length=100,unique=True,blank=True)
    time_period_of_creation = models.IntegerField(max_length=4,blank=True,default=2000)
    language = models.CharField(max_length=40,blank=True,choices=language_choices)
    publication_year = models.IntegerField(max_length=4,blank=True,default=2000)
    publisher = models.CharField(max_length=40,blank=True)
    description=models.TextField(max_length=200,blank=True)
    genre=models.CharField(max_length=22,choices=GENRE_CHOICES,blank=True)

    def __str__(self):
        return self.title + '('+str(self.author)+')'


class RentalBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    date_rental = models.DateField()
    date_return = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.book.title} - {self.user.username}"




class OverDue(models.Model):
    rental = models.OneToOneField(RentalBook, on_delete=models.CASCADE)
    date_overdue = models.DateField()


class Catalog(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('rented', 'Rented'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.OneToOneField(Books, on_delete=models.CASCADE)
    rental = models.OneToOneField(RentalBook, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')


    def is_available(self):
        return self.status == 'available'










