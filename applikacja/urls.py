from django.urls import path
from . import views


urlpatterns = [
    path("index/", views.index_page),
    path("about/", views.about_page, name='about_page'),
    path("contact/", views.contact_page, name='contact_page'),
    path("library/", views.Library.reading_page, name="reading_page"),
    path("login/", views.login_page, name="login_page"),
    path("register/", views.register_page, name="register_page"),
    path('catalog/', views.CatalogPage.book_list, name='catalog'),
    path('user_profile/', views.UserProfile.user_profile, name='user_profile'),
    path('logout/', views.logout_page, name='logout_page'),
    path('rent_book/', views.RentBookView.rent_book, name='rent_book'),
    path('return_book/', views.RentBookView.rent_book, name='return_book'),
    path('accounts/login/', views.login_page, name='login'),
]

