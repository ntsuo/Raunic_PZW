from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from .views import DjeloListView, UmjetnikListView, KulturniDogadajListView
from .views import UmjetnikDetailView, DjeloDetailView, KulturniDogadajDetailView
from .views import UmjetnikCreateView, DjeloCreateView, KulturniDogadajCreateView
from .views import DjeloUpdateView, UmjetnikUpdateView, KulturniDogadajUpdateView
from .views import DjeloDeleteView, UmjetnikDeleteView, KulturniDogadajDeleteView


app_name = 'main'  # here for namespacing of urls.

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'), 

    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('create-user/', views.create_user, name='create_user'),
    path('edit-user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),

    path('user-management/', views.user_management, name='user_management'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('login/', views.login_view, name='login'),

    path('djela/', DjeloListView.as_view(), name='djelo_list'),
    path('umjetnici/', UmjetnikListView.as_view(), name='umjetnik_list'),
    path('dogadaji/', KulturniDogadajListView.as_view(), name='dogadaj_list'),

    path('umjetnik/<int:pk>/', UmjetnikDetailView.as_view(), name='umjetnik_detail'),
    path('djelo/<int:pk>/', DjeloDetailView.as_view(), name='djelo_detail'),
    path('dogadaj/<int:pk>/', KulturniDogadajDetailView.as_view(), name='dogadaj_detail'),

    path('landing/', views.LandingPageView.as_view(), name='landing'),

    path('umjetnik/add/', UmjetnikCreateView.as_view(), name='umjetnik_form'),
    path('djelo/add/', DjeloCreateView.as_view(), name='djelo_form'),
    path('kulturnidogadaj/add/', KulturniDogadajCreateView.as_view(), name='kulturnidogadaj_form'),

    path('djelo/<int:pk>/update/', DjeloUpdateView.as_view(), name='djelo_update'),
    path('umjetnik/<int:pk>/update/', UmjetnikUpdateView.as_view(), name='umjetnik_update'),
    path('dogadaj/<int:pk>/update/', KulturniDogadajUpdateView.as_view(), name='dogadaj_update'),

    path('djelo/<int:pk>/delete/', DjeloDeleteView.as_view(), name='djelo_delete'),
    path('umjetnik/<int:pk>/delete/', UmjetnikDeleteView.as_view(), name='umjetnik_delete'),
    path('dogadaj/<int:pk>/delete/', KulturniDogadajDeleteView.as_view(), name='dogadaj_delete'),
]