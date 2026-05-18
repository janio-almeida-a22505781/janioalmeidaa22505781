from django import forms
from django.contrib.auth.models import User
from .models import Artigo, Comentario, Rating

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

class RatingForm(forms.ModelForm):

    pontuacao = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(1, 6)],
        widget=forms.RadioSelect,
        label='Nota'
    )

    class Meta:
        model = Rating
        fields = [
            'pontuacao'
        ]
        labels = {
            'pontuacao': 'Nota'
        }
        help_texts = {
            'pontuacao': 'Avalie este artigo de 1 a 5.'
        }
        widgets = {
            'pontuacao': forms.RadioSelect
        }
        
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