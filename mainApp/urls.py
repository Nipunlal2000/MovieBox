from django.urls import path
from . import views

urlpatterns = [

# <--===============================================================================================-->
#                                       USER
# <--===============================================================================================-->
    path('base', views.base,name='base'),
    path('home', views.Home,name='home'),
    path('create/', views.CreateMovie, name='create'),
    path('details/<int:movie_id>/', views.DetailsMovie,name='details'),
    path('update/<int:movie_id>/', views.UpdateMovie,name='update'),
    path('delete/<int:movie_id>/', views.DeleteMovie,name='delete'),
    path('search/', views.Search, name='search'),
    path('profile/', views.Profile, name='profile'),
    path('profile-update/', views.ProfileUpdate, name='profile-update'),
    path('rate/<int:movie_id>/', views.RateMovie, name='rate'),
    # <--===============================================================================================-->
#                                       REGISTRATION
# <--===============================================================================================-->

    path('', views.Index, name='index'),
    path('signup/', views.SignupPage, name='signup'),
    path('login/', views.LoginPage, name='login'),
    path('logout/', views.LogOut, name='logout'),
# <--===============================================================================================-->
#                                       ADMIN
# <--===============================================================================================-->

    path('admin-base/', views.AdminBase, name='admin-base'),
    path('admin-home/', views.AdminHome, name='admin-home'),
    path('admin-genre/', views.Genre, name='genre'),
    path('admin-create/', views.AdminCreateMovie, name='admin-create'),
    path('admin-delete/<int:movie_id>/', views.AdminDeleteMovie, name='admin-delete'),
    path('admin-search/', views.AdminSearch, name='admin-search'),
    path('admin-delete-user/<int:user_id>/', views.AdminDeleteUser, name='admin-delete-user'),

]
