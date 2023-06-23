from django.contrib import admin
from .models import Books, RentalBook, OverDue, Catalog


@admin.register(Books)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title',
                    'author']
    list_filter = [
                   'genre',
                   'language']
    search_fields = ['title',
                     'author']


@admin.register(RentalBook)
class RentalBookAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'book',
                    'date_rental',
                    'date_return']

    search_fields = ['user',
                     'book']


@admin.register(OverDue)
class OverDueAdmin(admin.ModelAdmin):
    list_display = ['rental',
                    'date_overdue']

@admin.register(Catalog)
class CatalogAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'book',
                    'status',
                    'rental',
                    ]
