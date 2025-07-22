from django.db import models
from django.utils.translation import gettext_lazy as _
#GENRE MODEL
MAX_GENRE_NAME_LENGTH = 200
MAX_GENRE_DISPLAY = 3

#BOOK MODEL
MAX_BOOK_TITLE_LENGTH = 200
MAX_BOOK_SUMMARY_LENGTH = 1000
MAX_BOOK_ISBN_LENGTH = 13

#BookInstance MODEL
BOOK_INSTANCE_IMPRINT_MAX_LENGTH = 200
BOOK_INSTANCE_STATUS_MAX_LENGTH = 1


class BOOK_INSTANCE_STATUS(models.TextChoices):
    MAINTENANCE = 'm', _('Maintenance')
    ON_LOAN = 'o', _('On loan')
    AVAILABLE = 'a', _('Available')
    RESERVED = 'r', _('Reserved')


#AUTHOR MODEL
MAX_AUTHOR_FIRST_NAME_LENGTH = 100
MAX_AUTHOR_LAST_NAME_LENGTH = 100

#GET_BOOKS_PER_PAGE
GET_BOOKS_PER_PAGE = 5

#PAGINATION 
PAGINATE_BY = 1

# Constants for bookin instance weekly renewal
WEEKLY_RENEWAL = 4

# Constants for date interval authorization
DATE_INTERVAL = {
    'date_of_death': '11/06/2020'
}
