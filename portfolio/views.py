from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import Group, User
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, ArtigoForm, ComentarioForm, RatingForm
from .models import Artigo, Comentario, Rating

def register_view(request):

    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )

            group, created = Group.objects.get_or_create(
                name='bloggers'
            )

            user.groups.add(group)

            login(request, user)

            return redirect('artigos')

    else:
        form = RegisterForm()

    return render(
        request,
        'portfolio/register.html',
        {'form': form}
    )

def artigos_view(request):

    artigos = Artigo.objects.all().order_by(
        '-data_criacao'
    )

    return render(
        request,
        'portfolio/artigos.html',
        {'artigos': artigos}
    )

@login_required
def criar_artigo(request):

    if request.method == 'POST':

        form = ArtigoForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            artigo = form.save(commit=False)

            artigo.autor = request.user

            artigo.save()

            return redirect('artigos')

    else:
        form = ArtigoForm()

    return render(
        request,
        'portfolio/criar_artigo.html',
        {'form': form}
    )

def artigo_detail(request, id):

    artigo = get_object_or_404(
        Artigo,
        id=id
    )

    comentario_form = ComentarioForm()
    rating_form = RatingForm()

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'comentario':
            comentario_form = ComentarioForm(request.POST)

            if comentario_form.is_valid():
                comentario = comentario_form.save(commit=False)
                comentario.artigo = artigo
                comentario.save()

                return redirect('artigo_detail', id=id)

        elif form_type == 'rating':
            rating_form = RatingForm(request.POST)

            if rating_form.is_valid():
                rating = rating_form.save(commit=False)
                rating.artigo = artigo
                rating.save()

                return redirect('artigo_detail', id=id)

    return render(
        request,
        'portfolio/artigo_detail.html',
        {
            'artigo': artigo,
            'comentario_form': comentario_form,
            'rating_form': rating_form
        }
    )

def landing_page(request):
    return render(request, 'portfolio/landing.html')


def logout_view(request):
    logout(request)
    return redirect('landing')

