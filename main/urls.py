from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from .views import DjeloListView, UmjetnikListView, KulturniDogadajListView
from .views import UmjetnikDetailView, DjeloDetailView, KulturniDogadajDetailView

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
]