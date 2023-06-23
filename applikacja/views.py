from .forms import CreateUserForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from .filters import BookFilter
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Books, RentalBook, Catalog
from django.utils import timezone
import datetime
import pdb


def index_page(request):
    return render(request, "index.html")


def about_page(request):
    return render(request, "about.html")


def contact_page(request):
    return render(request, "contact.html")


class Library:
    @staticmethod
    def reading_page(request):
        return render(request, 'library.html')

    @staticmethod
    def chart_view(request):
        genres = Books.objects.values('genre').annotate(count=Count('genre')).order_by('genre')
        genre_labels = [genre['genre'] for genre in genres]
        genre_values = [genre['count'] for genre in genres]

        languages = Books.objects.values('language').annotate(count=Count('language'))
        language_labels = [language['language'] for language in languages]
        language_values = [language['count'] for language in languages]

        return render(request, 'chart.html', {'genre_labels': genre_labels, 'genre_values': genre_values,
                                              'language_labels': language_labels, 'language_values': language_values})


def login_page(request):
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('user_profile')  # Przekieruj użytkownika do strony profilu użytkownika po zalogowaniu

    context = {'form': form}
    return render(request, 'login.html', context)


def register_page(request):
    form = CreateUserForm()
    if request.method=="POST":
        form= CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("user_profile")
    context= {'form': form}
    return render(request, 'register.html', context)


def logout_page(request):
    logout(request)
    return redirect('login_page')


class CatalogPage:
    @staticmethod
    def availability_status(request):
        catalog_entries = Catalog.objects.all()
        availability_list = [(entry.status, entry.book.title) for entry in catalog_entries]
        return render(request, 'catalog.html', {'availability_list': availability_list})

    def amount_book(request):
        amount_books = Books.objects.all().count()
        return render(request, 'catalog.html', {'amount_books': amount_books})

    def book_list(request):
        all_books = Books.objects.all()
        paginator = Paginator(all_books, 5)  # Podziel na strony, gdzie 10 to liczba elementów na stronę
        page_number = request.GET.get('page')  # Pobierz numer strony z parametru GET
        page_obj = paginator.get_page(page_number)  # Pobierz obiekt strony dla danego numeru
        return render(request, 'catalog.html', {'page_obj': page_obj})

    def filter_book(request):
        my_filter = BookFilter(request.GET, queryset=Books.objects.all())
        return render(request, 'catalog.html', {'my_filter': my_filter})


class UserProfile:

    @login_required
    def user_profile(request):
        user = request.user
        rental_books = RentalBook.objects.filter(user=user)
        rented_books_count = rental_books.count()
        rented_books_info = []
        wszystkie_ksiazki = Books.objects.all()

        for rental_book in rental_books:
            book = rental_book.book
            rental_info = {
                'book': book,
                'date_rental': rental_book.date_rental,
                'date_return': rental_book.date_return
            }
            rented_books_info.append(rental_info)

        context = {
            'user': user,
            'rented_books_count': rented_books_count,
            'rented_books_info': rented_books_info,
            'wszystkie_ksiazki': wszystkie_ksiazki,


        }
        return render(request, 'user_profile.html', context)


class RentBookView:

    @login_required
    def rent_book(request):
        if request.method == 'POST':
            book_id = request.POST.get('nazwa')
            book = Books.objects.get(id=book_id)
            date_rental = timezone.now().date()  # Aktualna data jako wartość daty (bez czasu)
            rental_book = RentalBook.objects.create(user=request.user, book=book, date_rental=date_rental, date_return=None)
            rental_book.save()
        return redirect('user_profile')


class ReturnBookView(View):
    @staticmethod
    @login_required
    def post(request):
        rental_book_id = request.POST.get('rental_book_id')
        print(rental_book_id)  # Debugging line
        if rental_book_id:
            try:
                rental_book = RentalBook.objects.get(id=rental_book_id)
                print(rental_book.book_id)  # Debugging line
                book_id = rental_book.book_id
                book = Books.objects.get(id=book_id)
                print(book.title)  # Debugging line
                if rental_book.user == request.user:
                    rental_book.date_return = timezone.now().date()
                    rental_book.save()
                    catalog = rental_book.catalog
                    catalog.status = 'available'
                    catalog.save()
                    return redirect('user_profile', rental_book.book.id)
            except RentalBook.DoesNotExist:
                print("RentalBook does not exist")  # Debugging line

        return render(request, 'user_profile.html')


