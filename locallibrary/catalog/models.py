from django.db import models
from django.urls import reverse # Used to generate URLs by reversing the URL patterns
import uuid
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from datetime import date

from utils.constants import (
    MAX_GENRE_NAME_LENGTH,
    MAX_GENRE_DISPLAY,
    MAX_BOOK_TITLE_LENGTH,
    MAX_BOOK_SUMMARY_LENGTH,
    MAX_BOOK_ISBN_LENGTH,
    BOOK_INSTANCE_IMPRINT_MAX_LENGTH,
    BOOK_INSTANCE_STATUS_MAX_LENGTH,
    BOOK_INSTANCE_STATUS,
    MAX_AUTHOR_FIRST_NAME_LENGTH,
    MAX_AUTHOR_LAST_NAME_LENGTH
) # Assuming you have a constants module for shared constants 
# Create your models here.
class Genre(models.Model):
    """Model representing a book genre."""
    name = models.CharField(
        max_length=MAX_GENRE_NAME_LENGTH, 
        help_text=_('Enter a book genre (e.g.Science Fiction)')
    )
    
    def __str__(self):
        """String for representing the Model object."""
        return self.name
    
class Book(models.Model):
    """Model representing a book (but not a specific copy of a book)."""
    title = models.CharField(
        max_length=MAX_BOOK_TITLE_LENGTH
    )
    author = models.ForeignKey(
        'Author', 
        on_delete=models.SET_NULL, 
        null=True
    )
    summary = models.TextField(
        max_length=MAX_BOOK_SUMMARY_LENGTH, 
        help_text=_('Enter a brief description of the book')
    )
    isbn = models.CharField(
        'ISBN', 
        max_length=MAX_BOOK_ISBN_LENGTH, 
        unique=True,
        help_text=_('13 Character '
        '<a href="https://www.isbn-international.org/content/what-isbn">' 
        'ISBN number'
        '</a>')
    )
    genre = models.ManyToManyField(
        Genre, 
        help_text=_('Select a genre for this book')
    )
    class Meta:
        ordering = ['title']
        permissions = (("can_see_all_books", "Can view all books in the catalog"),)

    def __str__(self):
        """String for representing the Model object."""
        return self.title
    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('book-detail', args=[str(self.id)])
    def display_genre(self):
        """Tạo một chuỗi cho Thể loại. Điều này là bắt buộc để hiển thị thể loại trong Admin."""
        return ', '.join(genre.name for genre in self.genre.all()[:MAX_GENRE_DISPLAY])


    display_genre.short_description = 'Genre'
    
class BookInstance(models.Model):
    """Model representing a specific copy of a book (i.e. that can be borrowed from the library)."""
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        help_text=_('Unique ID for this particular bookacross whole library')
    )
    book = models.ForeignKey(
        'Book', 
        on_delete=models.SET_NULL, null=True
    )
    borrower = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    imprint = models.CharField(
        max_length=BOOK_INSTANCE_IMPRINT_MAX_LENGTH
    )
    due_back = models.DateField(
        null=True, 
        blank=True
    )
    status = models.CharField(
        max_length=BOOK_INSTANCE_STATUS_MAX_LENGTH,
        choices=BOOK_INSTANCE_STATUS.choices,
        blank=True,
        default=BOOK_INSTANCE_STATUS.MAINTENANCE,
        help_text=_('Book availability'),
    )
    
    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Set book as returned"),)

    @property
    def is_overdue(self):
        """Kiểm tra xem sách có quá hạn hay không."""
        return self.due_back and date.today() > self.due_back
    
    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id} ({self.book.title})'
    
class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(
        max_length=MAX_AUTHOR_FIRST_NAME_LENGTH
    )
    last_name = models.CharField(
        max_length=MAX_AUTHOR_LAST_NAME_LENGTH
    )
    date_of_birth = models.DateField(
        null=True, 
        blank=True
    )
    date_of_death = models.DateField(
        'Died', 
        null=True, 
        blank=True
    )

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])
    def __str__(self):
        """String for representing the Model object."""
        return f'{self.last_name}, {self.first_name}'
