from django.contrib import admin
from .models import Author, Genre, Book, BookInstance # Từ các mô hình của bạn, nhập các lớp Author, Genre, Book, BookInstance

# Register your models here.

# admin.site.register(Book) # Đăng ký mô hình Book với trang admin
# admin.site.register(Author) # Đăng ký mô hình Author với trang admin
admin.site.register(Genre) # Đăng ký mô hình Genre với trang admin
# admin.site.register(BookInstance) # Đăng ký mô hình BookInstance với trang admin
class BookInline(admin.TabularInline):
    model = Book
    extra = 0  # Số lượng bản ghi trống để hiển thị trong admin

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines = [BookInline]

# Đăng ký lớp admin với mô hình liên quan
admin.site.register(Author, AuthorAdmin)
    
class BooksInstanceInline(admin.TabularInline):
    model = BookInstance

# Đăng ký lớp Admin cho Book sử dụng decorator
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BooksInstanceInline]

# Đăng ký lớp Admin cho BookInstance sử dụng decorator
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_filter = ('status', 'due_back')
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back')
        }),
    )
    