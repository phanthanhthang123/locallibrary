from django.shortcuts import render
from catalog.models import Book, BookInstance, Author, Genre
from django.views import generic
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
from catalog.forms import RenewBookForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from utils.constants import DATE_INTERVAL

from utils.constants import (
    BOOK_INSTANCE_STATUS,
    GET_BOOKS_PER_PAGE,
    PAGINATE_BY
    )

# Create your views here.
# @permission_required('catalog.can_mark_returned')
# @permission_required('catalog.can_edit')
# @login_required
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
    
    #Number of visits to this page
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    contexts = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=contexts)

class BookListView(PermissionRequiredMixin,LoginRequiredMixin,generic.ListView):
    model = Book
    paginate_by = PAGINATE_BY  # Number of books to display per page
    context_object_name = 'my_book_list' # your own name for the list as a template variable
    queryset = Book.objects.all()[:GET_BOOKS_PER_PAGE]  # Get 5 books containing 'war' in the title
    template_name = 'catalog/book_list.html'  # Specify your own template name/location
    permission_required = 'catalog.can_see_all_books'  # Specify the permission required to view this page

    def get_context_data(self, **kwargs):
        # Gọi phương thức triển khai ở lớp cha trước để lấy context
        context = super(BookListView, self).get_context_data(**kwargs)
        # Thêm dữ liệu tùy biến
        context['total_books'] = Book.objects.count()
        context['genres'] = Genre.objects.all()
        context['is_logged_in'] = self.request.user.is_authenticated
        return context

class BookDetailView(PermissionRequiredMixin,LoginRequiredMixin,generic.DetailView):
    model = Book
    template_name = 'catalog/book_detail.html'  # Specify your own template name/location
    context_object_name = 'book'  # your own name for the book as a template variable
    permission_required = 'catalog.can_see_all_books'

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
    
class AuthorListView(PermissionRequiredMixin,LoginRequiredMixin,generic.ListView):
    model = Author
    template_name = 'catalog/author_list.html'  # Specify your own template name/location
    context_object_name = 'author_list'  # your own name for the list as a template variable
    permission_required = 'catalog.can_see_all_authors'

    def get_context_data(self, **kwargs):
        # Gọi phương thức triển khai ở lớp cha trước để lấy context
        context = super(AuthorListView, self).get_context_data(**kwargs)
        context['total_authors'] = Author.objects.count()
        return context

@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    """View function for renewing a specific book instance by librarian."""
    book_instance = BookInstance.objects.get(pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':
        form = RenewBookForm(request.POST)
        if form.is_valid():
            # Process the data in form.cleaned_data
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()
            # Redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed'))
    else:
        # If this is a GET (or any other method) create the default form.
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})
    
    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context=context)

@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def all_borrowed(request):
    """View to show all borrowed books (admin/librarian view)."""
    borrowed_books = BookInstance.objects.filter(status__exact='o').order_by('due_back')
    context = {
        'borrowed_books': borrowed_books
    }
    return render(request, 'catalog/all_borrowed_list.html', context)

class AuthorCreate(CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = DATE_INTERVAL

class AuthorUpdate(UpdateView):
    model = Author
    fields =  ['first_name', 'last_name', 'date_of_birth', 'date_of_death']

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')

class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = 'catalog/author_detail.html'  # Specify your own template name/location
    context_object_name = 'author'  # your own name for the author as a template variable

    def get_context_data(self, **kwargs):
        # Gọi phương thức triển khai ở lớp cha trước để lấy context
        context = super(AuthorDetailView, self).get_context_data(**kwargs)
        context['book_list'] = self.object.book_set.all()  # Lấy tất cả Book liên quan đến Author này
        return context
