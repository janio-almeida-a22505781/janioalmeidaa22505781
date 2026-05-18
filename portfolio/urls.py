from django.urls import path
from django.contrib.auth import views as auth_views
from .views import landing_page, register_view, artigos_view, criar_artigo, artigo_detail, logout_view

urlpatterns = [
    path('', landing_page, name='landing'),
    path('register/', register_view, name='register'),
    path('artigos/', artigos_view, name='artigos'),
    path('artigos/criar/', criar_artigo, name='criar_artigo'),
    path('login/', auth_views.LoginView.as_view(template_name='portfolio/login.html'), name='login'),
    path('logout/', logout_view, name='logout'),
    path('artigos/<int:id>/', artigo_detail, name='artigo_detail'),
]