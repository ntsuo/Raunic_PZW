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
from django.views.generic.edit import CreateView
from .forms import UmjetnikForm, DjeloForm, KulturniDogadajForm
from django.views import View
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import UpdateView
from django.views.generic.edit import DeleteView
from django.http import HttpResponseForbidden

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
@user_passes_test(is_regular_user) #ako je admin?
def user_dashboard(request):
    return render(request, 'main/user_dashboard.html')

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
        naslov = self.request.GET.get('naslov')
        medij = self.request.GET.get('medij')

        if naslov:
            queryset = queryset.filter(naslov__icontains=naslov)
        if medij:
            queryset = queryset.filter(medij__icontains=medij)

        return queryset

class UmjetnikListView(ListView):
    model = Umjetnik
    template_name = 'main/umjetnik_list.html'
    context_object_name = 'umjetnici'

    def get_queryset(self):
        queryset = Umjetnik.objects.all()
        ime_prezime_filter = self.request.GET.get('q')
        sortiranje = self.request.GET.get('sort')
        if ime_prezime_filter:
            queryset = queryset.filter(
                Q(ime__icontains=ime_prezime_filter) | Q(prezime__icontains=ime_prezime_filter)
            )
        if sortiranje:
            if sortiranje == 'ime':
                queryset = queryset.order_by('ime')
            elif sortiranje == 'prezime':
                queryset = queryset.order_by('prezime')

        return queryset


class KulturniDogadajListView(ListView):
    model = KulturniDogadaj
    template_name = 'main/dogadaj_list.html'
    context_object_name = 'dogadaji'

    def get_queryset(self):
        queryset = KulturniDogadaj.objects.all()
        datum_filter = self.request.GET.get('datum')
        lokacija_filter = self.request.GET.get('lokacija')
        ime_filter = self.request.GET.get('ime')

        if datum_filter:
            queryset = queryset.filter(datum=datum_filter)
        if lokacija_filter:
            queryset = queryset.filter(lokacija__icontains=lokacija_filter)
        if ime_filter:
            queryset = queryset.filter(ime__icontains=ime_filter)

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

### LANDING PAGE
class LandingPageView(View):
    def get(self, request, *args, **kwargs):
        if not is_admin(request.user):
            return HttpResponseForbidden("Nemate dopuštenje za pristup ovoj stranici.")
        return render(request, 'main/landing.html')
    
@user_passes_test(is_admin)
def landing_page(request):
    return render(request, 'main/landing.html')

### CRUD AKCIJE

# CREATE
class UmjetnikCreateView(CreateView):
    model = Umjetnik
    form_class = UmjetnikForm
    template_name = 'main/umjetnik_form.html'

    def get_success_url(self):
        return reverse('main:umjetnik_detail', kwargs={'pk': self.object.pk})

class DjeloCreateView(CreateView):
    model = Djelo
    form_class = DjeloForm
    template_name = 'main/djelo_form.html'

    def get_success_url(self):
        return reverse('main:djelo_detail', kwargs={'pk': self.object.pk})

class KulturniDogadajCreateView(CreateView):
    model = KulturniDogadaj
    form_class = KulturniDogadajForm
    template_name = 'main/kulturnidogadaj_form.html'

    def get_success_url(self):
        return reverse('main:dogadaj_detail', kwargs={'pk': self.object.pk})
    
# UPDATE
class DjeloUpdateView(UpdateView):
    model = Djelo
    form_class = DjeloForm
    template_name = 'main/djelo_update.html'
    context_object_name = 'djelo'

    def get_success_url(self):
        return reverse('main:djelo_detail', kwargs={'pk': self.object.pk})
    
    def dispatch(self, request, *args, **kwargs):
        if not is_admin(request.user): 
            return HttpResponseForbidden("Nemate dopuštenje za uređivanje ovog objekta.")
        return super().dispatch(request, *args, **kwargs)

class UmjetnikUpdateView(UpdateView):
    model = Umjetnik
    form_class = UmjetnikForm
    template_name = 'main/umjetnik_update.html'
    context_object_name = 'umjetnik'

    def get_success_url(self):
        return reverse('main:umjetnik_detail', kwargs={'pk': self.object.pk})
    
    def dispatch(self, request, *args, **kwargs):
        if not is_admin(request.user): 
            return HttpResponseForbidden("Nemate dopuštenje za uređivanje ovog objekta.")
        return super().dispatch(request, *args, **kwargs)
    
class KulturniDogadajUpdateView(UpdateView):
    model = KulturniDogadaj
    form_class = KulturniDogadajForm
    template_name = 'main/dogadaj_update.html'
    context_object_name = 'dogadaj'

    def get_success_url(self):
        return reverse('main:dogadaj_detail', kwargs={'pk': self.object.pk})
    
    def dispatch(self, request, *args, **kwargs):
        if not is_admin(request.user): 
            return HttpResponseForbidden("Nemate dopuštenje za uređivanje ovog objekta.")
        return super().dispatch(request, *args, **kwargs)

# DELETE

class DjeloDeleteView(DeleteView):
    model = Djelo
    template_name = 'main/djelo_delete.html'
    success_url = reverse_lazy('main:djelo_list')

    def dispatch(self, request, *args, **kwargs):
        if not is_admin(request.user): 
            return HttpResponseForbidden("Nemate dopuštenje za brisanje ovog objekta.")
        return super().dispatch(request, *args, **kwargs)

class UmjetnikDeleteView(DeleteView):
    model = Umjetnik
    template_name = 'main/umjetnik_delete.html'
    success_url = reverse_lazy('main:umjetnik_list')

    def dispatch(self, request, *args, **kwargs):
        if not is_admin(request.user): 
            return HttpResponseForbidden("Nemate dopuštenje za brisanje ovog objekta.")
        return super().dispatch(request, *args, **kwargs)

class KulturniDogadajDeleteView(DeleteView):
    model = KulturniDogadaj
    template_name = 'main/dogadaj_delete.html'
    success_url = reverse_lazy('main:dogadaj_list')

    def dispatch(self, request, *args, **kwargs):
        if not is_admin(request.user): 
            return HttpResponseForbidden("Nemate dopuštenje za brisanje ovog objekta.")
        return super().dispatch(request, *args, **kwargs)