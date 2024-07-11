from django.contrib import messages
from django.contrib.auth import logout
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from django.shortcuts import render, redirect
from .forms import *
from .models import UserProfile, LoginTable


# Create your views here.

def Index(request):
    return render(request, 'index.html',)

# <--===============================================================================================-->
#                                       USER
# <--===============================================================================================-->


def base(request):
    user_name = request.session['username']

    return render(request, 'user/base.html', {'user_name': user_name})


def Home(request):
    user_name = request.session['username']
    movies = Movie.objects.all()

    for movie in movies:
        try:
            review = Review.objects.get(movie=movie)
            movie.rating = review.rating
        except Review.DoesNotExist:
            movie.rating = None

    paginator=Paginator(movies,4)
    page_number= request.GET.get('page')

    try:
        page=paginator.get_page(page_number)

    except EmptyPage:
        page=paginator.page(page_number.num_pages)


    return render(request, 'user/home.html', {'movies': movies, 'user_name': user_name,'page':page})


def CreateMovie(request):
    genres = Genres.objects.all()

    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)

        if form.is_valid():
            movie = form.save(commit=False)
            movie.added_by = LoginTable.objects.get(username=request.session['username'])
            movie.save()
            return redirect('home')
    else:
        form = MovieForm()

    return render(request, 'user/create-movie.html', {'form': form, 'genres': genres})


def DetailsMovie(request, movie_id):
    user_name = request.session['username']
    movie = Movie.objects.get(id=movie_id)

    return render(request, 'user/detail-movie.html', {'movie': movie, 'user_name': user_name})


def UpdateMovie(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    genres = Genres.objects.all()

    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = MovieForm(instance=movie)

    return render(request, 'user/update-movie.html', {'form': form, 'genres': genres, 'movie': movie})


def RateMovie(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    user = LoginTable.objects.get(username=request.session['username'])

    try:
        review = Review.objects.get(movie=movie,user=user)
    except Review.DoesNotExist:
        review = None

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)

        if form.is_valid():
            review = form.save(commit=False)
            review.movie = movie
            review.user = user
            review.save()
            return redirect('home')
    else:
        form = ReviewForm(instance=review)
    context = {'form': form,
               'movie':movie,
               'review': review}
    return render(request, 'user/rate.html', context)


def DeleteMovie(request, movie_id):
    user_name = request.session['username']
    if not user_name:
        return redirect('/')

    movie = Movie.objects.get(id=movie_id)

    if user_name != movie.added_by.username:
        return redirect('home')

    if request.method == 'POST':
        movie.delete()
        return redirect('home')

    return render(request, 'user/delete-movie.html', {'movie': movie, 'user_name': user_name})


def Search(request):
    user_name = request.session['username']

    query = None
    movies = None

    if 'q' in request.GET:

        query = request.GET.get('q')
        movies = Movie.objects.filter(Q(title__icontains=query))
    else:
        movies = []

    context= {'movies': movies,
              'query': query,
              'user_name': user_name}
    return render(request, 'user/search-movie.html', context)


def Profile(request):
    if 'username' not in request.session:
        return redirect('login')

    user_name = request.session['username']
    first_name = request.session['firstname']
    last_name = request.session['lastname']
    e_mail = request.session['email']

    context = {'user_name': user_name,
               'first_name': first_name,
               'last_name': last_name,
               'e_mail': e_mail}
    return render(request, 'user/profile.html', context)


def ProfileUpdate(request):
    if 'username' not in request.session:
        return redirect('login')

    user_name = request.session['username']
    userprofile = UserProfile.objects.get(username=request.session['username'])

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=userprofile)

        if form.is_valid():
            form.save()

            request.session['username'] = userprofile.username
            request.session['firstname'] = userprofile.firstname
            request.session['lastname'] = userprofile.lastname
            request.session['email'] = userprofile.email

            return redirect('profile')
    else:
        form = UserProfileForm(instance=userprofile)

    context = {'form': form,
               'user_name':user_name}
    return render(request,'user/profile-update.html', context)



# <--===============================================================================================-->
#                                       REGISTRATION
# <--===============================================================================================-->

def SignupPage(request):
    login_table = LoginTable()
    userprofile = UserProfile()

    if request.method == 'POST':

        userprofile.username = request.POST['username']
        userprofile.password = request.POST['password']
        userprofile.password2 = request.POST['password2']
        userprofile.firstname = request.POST['firstname']
        userprofile.lastname = request.POST['lastname']
        userprofile.email = request.POST['email']

        login_table.username = request.POST['username']
        login_table.password = request.POST['password']
        login_table.password2 = request.POST['password2']
        login_table.firstname = request.POST['firstname']
        login_table.lastname = request.POST['lastname']
        login_table.email = request.POST['email']
        login_table.type = 'user'

        if request.POST['password'] == request.POST['password2']:
            userprofile.save()
            login_table.save()

            messages.info(request, 'Registration success')
            return redirect('login')

        else:
            messages.info(request, 'Password not matching')
            return redirect('signup')

    return render(request, 'registration/signup.html')


def LoginPage(request):
    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']
        try:
            user = LoginTable.objects.filter(username=username, password=password, type='user').exists()

            if user is not None:

                user_details = LoginTable.objects.get(username=username, password=password)
                user_name = user_details.username
                first_name = user_details.firstname
                last_name = user_details.lastname
                e_mail = user_details.email
                type = user_details.type

                if type == 'user':
                    request.session['username'] = user_name
                    request.session['firstname'] = first_name
                    request.session['lastname'] = last_name
                    request.session['email'] = e_mail

                    return redirect('home')  # user_dashboard

                elif type == 'admin':
                    request.session['username'] = user_name
                    request.session['firstname'] = first_name
                    request.session['lastname'] = last_name
                    request.session['email'] = e_mail

                    return redirect('admin-home')  # admin_dashboard

            else:
                messages.error(request, 'invalid username or password')

        except:
            messages.error(request, 'invalid role')

    return render(request, 'registration//login.html')


def LogOut(request):
    logout(request)
    return render(request, 'login.html')


# <--===============================================================================================-->
#                                       ADMIN
# <--===============================================================================================-->


def AdminBase(request):
    user_name = request.session['username']

    return render(request, 'mainAdmin/admin-base.html', {'user_name': user_name})


def AdminHome(request):
    user_name = request.session['username']
    movies = Movie.objects.all()
    users = LoginTable.objects.filter(type='user')

    paginator=Paginator(users,4)
    page_number= request.GET.get('page')

    try:
        page=paginator.get_page(page_number)

    except EmptyPage:
        page=paginator.page(page_number.num_pages)

    context = {'movies': movies,
               'user_name': user_name,
               'users':users,
               'page':page}
    return render(request, 'mainAdmin/admin-home.html', context)


def Genre(request):
    if request.method == 'POST':
        form = GenreForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('admin-create')
    else:
        form = GenreForm()

    return render(request, 'mainAdmin/genre.html', {'form': form})


def AdminCreateMovie(request):
    genres = Genres.objects.all()
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)

        if form.is_valid():
            movie = form.save(commit=False)
            movie.added_by = LoginTable.objects.get(username=request.session['username'])
            movie.save()
            return redirect('admin-home')
    else:
        form = MovieForm()

    return render(request, 'mainAdmin/admin-create-movie.html', {'form': form, 'genres': genres})


def AdminDeleteMovie(request, movie_id):
    user_name = request.session['username']

    movie = Movie.objects.get(id=movie_id)

    if request.method == 'POST':
        movie.delete()
        return redirect('admin-home')

    return render(request, 'mainAdmin/admin-delete-movie.html', {'movie': movie, 'user_name': user_name})


def AdminDeleteUser(request, user_id):
    user_name = request.session['username']
    user = LoginTable.objects.get(id=user_id)

    if request.method == 'POST':
        user.delete()
        return redirect('admin-home')

    return render(request, 'mainAdmin/admin-delete-movie.html', {'user': user, 'user_name': user_name})



def AdminSearch(request):
    user_name = request.session.get('username')
    query = request.GET.get('q', '')

    if query:
        users = LoginTable.objects.filter(Q(username__icontains=query) & Q(type='user'))
    else:
        users = LoginTable.objects.filter(type='user')

    # Pagination
    paginator = Paginator(users,4)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'query': query,
        'user_name': user_name,
        'page': page,
    }

    return render(request, 'mainAdmin/admin-search-user.html', context)

