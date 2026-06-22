from django import forms
from django.core.exceptions import ValidationError
from .models import User, Etablissement


class InscriptionEtablissementForm(forms.Form):
    # --- Établissement ---
    nom = forms.CharField(
        max_length=200,
        label="Nom de l'établissement",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: École Primaire Cheikh Anta Diop'})
    )
    type_etablissement = forms.ChoiceField(
        choices=Etablissement.TYPE_CHOICES,
        label="Type d'établissement",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    region = forms.CharField(
        max_length=100,
        label="Région",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Dakar'})
    )
    departement = forms.CharField(
        max_length=100, required=False,
        label="Département",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Pikine'})
    )
    commune = forms.CharField(
        max_length=100, required=False,
        label="Commune",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Thiaroye'})
    )
    telephone_etablissement = forms.CharField(
        max_length=20, required=False,
        label="Téléphone de l'établissement",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: +221 33 XXX XX XX'})
    )
    email_etablissement = forms.EmailField(
        required=False,
        label="Email de l'établissement",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'contact@ecole.sn'})
    )

    # --- Compte administrateur ---
    prenom = forms.CharField(
        max_length=150,
        label="Prénom du directeur / responsable",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénom'})
    )
    nom_directeur = forms.CharField(
        max_length=150,
        label="Nom du directeur / responsable",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom de famille'})
    )
    email = forms.EmailField(
        label="Email du responsable",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'directeur@ecole.sn'})
    )
    telephone = forms.CharField(
        max_length=20, required=False,
        label="Téléphone du responsable",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+221 7X XXX XX XX'})
    )
    username = forms.CharField(
        max_length=150,
        label="Identifiant de connexion",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: ecole_ced_dakar'})
    )
    password1 = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Minimum 8 caractères'})
    )
    password2 = forms.CharField(
        label="Confirmer le mot de passe",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Répéter le mot de passe'})
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError("Cet identifiant est déjà utilisé. Veuillez en choisir un autre.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Un compte existe déjà avec cette adresse email.")
        return email

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password1')
        p2 = cleaned.get('password2')
        if p1 and p2 and p1 != p2:
            self.add_error('password2', "Les deux mots de passe ne correspondent pas.")
        if p1 and len(p1) < 8:
            self.add_error('password1', "Le mot de passe doit contenir au moins 8 caractères.")
        return cleaned

    def save(self):
        data = self.cleaned_data
        user = User.objects.create_user(
            username=data['username'],
            password=data['password1'],
            email=data['email'],
            first_name=data['prenom'],
            last_name=data['nom_directeur'],
            telephone=data.get('telephone', ''),
            role='admin',
        )
        etablissement = Etablissement.objects.create(
            nom=data['nom'],
            type_etablissement=data['type_etablissement'],
            region=data['region'],
            departement=data.get('departement', ''),
            commune=data.get('commune', ''),
            telephone=data.get('telephone_etablissement', ''),
            email=data.get('email_etablissement', ''),
            directeur=user,
        )
        return user, etablissement
