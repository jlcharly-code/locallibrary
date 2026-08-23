from django.db import models
from django.urls import reverse  # Cette fonction est utilisée pour formater les URL
from django.conf import settings
from datetime import date
import uuid  # Ce module est nécessaire à la gestion des identifiants unique (RFC 4122) pour les copies des livres

class Book(models.Model):
    """Cet objet représente un livre (mais ne traite pas les copies présentes en rayon)."""
    title = models.CharField('titre', max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True, verbose_name='auteur')
    summary = models.TextField('résumé', max_length=1000, help_text='Entrer une brève description du livre')
    isbn = models.CharField('ISBN', max_length=13, help_text='Numéro ISBN à 13 caractères')
    genre = models.ManyToManyField('Genre', verbose_name='genre', help_text='Sélectionner un genre pour ce livre')
    language = models.CharField('langue', max_length=50, blank=True, default='français', help_text='Langue du livre (ex: français, anglais, espagnol)')
    cover_image = models.ImageField('couverture', upload_to='covers/', blank=True, null=True, help_text='Couverture du livre')

    class Meta:
        verbose_name = 'livre'
        verbose_name_plural = 'livres'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return ', '.join(genre.name for genre in self.genre.all()[:5])
    display_genre.short_description = 'Genre'


class Genre(models.Model):
    """Cet objet représente une catégorie ou un genre littéraire."""
    name = models.CharField('nom', max_length=200, help_text='Entrer un genre littéraire (ex. Science-fiction)')

    class Meta:
        verbose_name = 'genre'
        verbose_name_plural = 'genres'

    def __str__(self):
        return self.name


class BookInstance(models.Model):
    """Cet objet permet de modéliser les copies d'un ouvrage (i.e. qui peut être emprunté)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Identifiant unique pour cette copie dans toute la bibliothèque')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True, verbose_name='livre')
    imprint = models.CharField('édition', max_length=200)
    due_back = models.DateField('date de retour prévue', null=True, blank=True)
    borrower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='emprunteur')

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'Emprunté'),
        ('a', 'Disponible'),
        ('r', 'Réservé'),
    )

    status = models.CharField('statut', max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Disponibilité du livre')

    @property
    def is_overdue(self):
        """Détermine si le livre est en retard selon la date d'échéance et la date du jour."""
        return bool(self.due_back and date.today() > self.due_back)

    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Livre rendu"),)
        verbose_name = 'exemplaire'
        verbose_name_plural = 'exemplaires'

    def __str__(self):
        return f'{self.id} ({self.book.title})'


class Author(models.Model):
    """Cet objet représente un auteur."""
    first_name = models.CharField('prénom', max_length=100)
    last_name = models.CharField('nom', max_length=100)
    date_of_birth = models.DateField('date de naissance', null=True, blank=True)
    date_of_death = models.DateField('décès', null=True, blank=True)
    bio = models.TextField('biographie', max_length=1000, help_text='Entrer une petite bio')

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = 'auteur'
        verbose_name_plural = 'auteurs'

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'
    