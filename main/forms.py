from django import forms
from main.models import CustomUser, Djelo, Umjetnik, KulturniDogadaj
from django.contrib.auth.forms import UserCreationForm

class UserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser  
        fields = ('username', 'email')  


#######

class UmjetnikForm(forms.ModelForm):
    class Meta:
        model = Umjetnik
        fields = ['ime', 'prezime', 'biografija', 'slike_umjetnika']

    ### validacija contenta
    def clean_ime(self):
        ime = self.cleaned_data.get('ime')
        if not ime.isalpha():
            raise forms.ValidationError("Ime može sadržavati samo slova.")
        return ime

    def clean_prezime(self):
        prezime = self.cleaned_data.get('prezime')
        if len(prezime) < 2:
            raise forms.ValidationError("Prezime mora imati najmanje 2 slova.")
        return prezime

class DjeloForm(forms.ModelForm):
    class Meta:
        model = Djelo
        fields = ['naslov', 'umjetnik', 'opis', 'slika', 'medij']

class KulturniDogadajForm(forms.ModelForm):
    class Meta:
        model = KulturniDogadaj
        fields = ['ime', 'opis', 'datum', 'vrijeme', 'lokacija', 'organizator', 'umjetnicka_djela']
        widgets = {
            'datum': forms.DateInput(attrs={'type': 'date'}),
            'vrijeme': forms.TimeInput(attrs={'type': 'time'})
            }
     