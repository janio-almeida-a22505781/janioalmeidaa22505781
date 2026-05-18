from django import forms
from django.contrib.auth.models import User
from .models import Artigo, Comentario

class ArtigoForm(forms.ModelForm):

    class Meta:
        model = Artigo

        fields = [
            'titulo',
            'conteudo',
            'imagem',
            'link',
        ]

class ComentarioForm(forms.ModelForm):

    class Meta:
        model = Comentario

        fields = [
            'autor',
            'texto'
        ]
        
class RegisterForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput
    )

    class Meta:
        model = User

        fields = [
            'username',
            'email',
            'password'
        ]
    
    def save(self, commit=True):
        # Não salva automaticamente, pois a view usa create_user()
        return None