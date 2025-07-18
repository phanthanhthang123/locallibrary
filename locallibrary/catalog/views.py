from django.shortcuts import render
from catalog.models import Book, BookInstance, Author, Genre
from django.views import generic
from utils.constants import (
    BOOK_INSTANCE_STATUS,
    GET_BOOKS_PER_PAGE,
    PAGINATE_BY
    )

# Create your views here.
def index(request):
    """View function for home page of site."""
    # Generate counts of some of the main objects
    num_books = Book.objects.count()
    num_instances = BookInstance.objects.count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(
        status__exact=BOOK_INSTANCE_STATUS.AVAILABLE
    ).count()

    # The 'all()' is implied by default
    num_authors = Author.objects.count()  # The 'all()' is implied by default
    
    contexts = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=contexts)

class BookListView(generic.ListView):
    model = Book
    paginate_by = PAGINATE_BY  # Number of books to display per page
    context_object_name = 'my_book_list' # your own name for the list as a template variable
    queryset = Book.objects.all()[:GET_BOOKS_PER_PAGE]  # Get 5 books containing 'war' in the title
    template_name = 'catalog/book_list.html'  # Specify your own template name/location

    def get_context_data(self, **kwargs):
        # Gọi phương thức triển khai ở lớp cha trước để lấy context
        context = super(BookListView, self).get_context_data(**kwargs)
        # Thêm dữ liệu tùy biến
        context['total_books'] = Book.objects.count()
        context['genres'] = Genre.objects.all()
        context['is_logged_in'] = self.request.user.is_authenticated
        return context

class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'catalog/book_detail.html'  # Specify your own template name/location
    context_object_name = 'book'  # your own name for the book as a template variable
    def get_context_data(self, **kwargs):
        # Gọi phương thức triển khai ở lớp cha trước để lấy context
        context = super(BookDetailView, self).get_context_data(**kwargs)
        book = self.object
        # Thêm dữ liệu tùy biến
        context['book_genre'] = book.genre.all()  # Lấy tất cả Genre liên quan đến Book này
        context['bookinstance_set'] = book.bookinstance_set.all()  # Lấy tất cả BookInstance liên quan đến Book này
        context['available_copies'] = book.bookinstance_set.filter(
            status=BOOK_INSTANCE_STATUS.AVAILABLE
        ).count()
        context['copies_available'] = BOOK_INSTANCE_STATUS.AVAILABLE
        context['copies_maintenance'] = BOOK_INSTANCE_STATUS.MAINTENANCE
        return context
