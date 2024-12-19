from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
from .models import CustomUser
from main.forms import UserEditForm, CustomUserCreationForm
from django.views.generic import ListView
from django.db.models import Q
from .models import Djelo, Umjetnik, KulturniDogadaj
from django.views.generic.detail import DetailView

# provjera je li osoba administrator
def is_admin(user):
    return user.is_superuser or user.groups.filter(name='Administrator').exists()

# provjera je li korisnik
def is_regular_user(user):
    return user.groups.filter(name='Korisnik').exists()

@login_required
def index(request):
    return render(request, 'main/index.html')


@user_passes_test(is_admin)
def admin_dashboard(request):
    users = CustomUser.objects.all()
    return render(request, 'main/admin_dashboard.html', {'users': users})

@user_passes_test(is_admin)
def create_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST['role']

        user = CustomUser.objects.create_user(username=username, password=password)
        group = Group.objects.get(name=role)
        user.groups.add(group)
        user.save()
        return redirect('admin_dashboard')

    return render(request, 'main/create_user.html')

@user_passes_test(is_admin)
def edit_user(request, user_id):


    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()  
            messages.success(request, f"User '{user.username}' has been updated successfully!")
            return redirect('user_management')
    else:
        # prikaz
        form = UserEditForm(instance=user)

    return render(request, 'main/edit_user.html', {'form': form, 'user': user})


@user_passes_test(is_admin)
def delete_user(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    user.delete()
    return redirect('admin_dashboard')


# pogled korisnika
@user_passes_test(is_regular_user)
def user_dashboard(request):
    return render(request, 'user_dashboard.html')

@login_required
def user_management(request):
    
    users = CustomUser.objects.all()  # prikazuje sve korisnike
    return render(request, 'main/user_management.html', {'users': users})

##########################

#def index(request):
    return render(request, 'main/index.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST) 

        if form.is_valid():
            user = form.save()

            # uzima korisničko ime i lozinku
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            # autentifikacija 
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user) 
                return redirect('main:index') 

    else:
        form = CustomUserCreationForm() 
    context = {'form': form}

    return render(request, 'registration/register.html', context)

def login_view(request):
    if request.method == 'POST':
        pass  

    return render(request, 'registration/login.html')  

## LISTVIEW-SI

class DjeloListView(ListView):
    model = Djelo
    template_name = 'main/djelo_list.html' 
    context_object_name = 'djela'
    paginate_by = 10 

    def get_queryset(self):
        queryset = Djelo.objects.all()
        naslov= self.request.GET.get('naslov') 
        if naslov:
            queryset = queryset.filter(naslov__icontains=naslov)
        return queryset


class UmjetnikListView(ListView):
    model = Umjetnik
    template_name = 'main/umjetnik_list.html'
    context_object_name = 'umjetnici'

    def get_queryset(self):
        queryset = Umjetnik.objects.all()
        ime_prezime_filter = self.request.GET.get('q')
        if ime_prezime_filter:
            queryset = queryset.filter(
                Q(ime__icontains=ime_prezime_filter) | Q(prezime__icontains=ime_prezime_filter)
            )
        return queryset


class KulturniDogadajListView(ListView):
    model = KulturniDogadaj
    template_name = 'main/dogadaj_list.html'
    context_object_name = 'dogadaji'

    def get_queryset(self):
        queryset = KulturniDogadaj.objects.all()
        datum_filter = self.request.GET.get('datum')
        if datum_filter:
            queryset = queryset.filter(datum=datum_filter)
        return queryset
    
## DETAILVIEW-SI
class UmjetnikDetailView(DetailView):
    model = Umjetnik
    template_name = 'main/umjetnik_detail.html' 
    context_object_name = 'umjetnik' 

class DjeloDetailView(DetailView):
    model = Djelo
    template_name = 'main/djelo_detail.html' 
    context_object_name = 'djelo'

class KulturniDogadajDetailView(DetailView):
    model = KulturniDogadaj
    template_name = 'main/dogadaj_detail.html'
    context_object_name = 'dogadaj'