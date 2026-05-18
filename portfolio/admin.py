from django.contrib import admin

from .models import Licenciatura
from .models import UnidadeCurricular
from .models import Projeto
from .models import Tecnologia
from .models import Competencia
from .models import Formacao
from .models import TFC
from .models import ExperienciaProfissional
from .models import MakingOf
    
# Register your models here.

@admin.register(Licenciatura)
class LicenciaturaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'universidade', 'duracao_anos')
    search_fields = ('nome', 'universidade')

@admin.register(UnidadeCurricular)
class UnidadeCurricularAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ano', 'semestre', 'licenciatura')
    search_fields = ('nome', 'codigo', 'docente')
    list_filter = ('ano', 'semestre')

@admin.register(Projeto)
class ProjetoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'unidade_curricular', 'data_criacao')
    search_fields = ('nome', 'descricao')
    list_filter = ('unidade_curricular',)

@admin.register(Tecnologia)
class TecnologiaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'nivel')
    search_fields = ('nome',)
    list_filter = ('nivel',)

@admin.register(Competencia)
class CompetenciaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'nivel')
    search_fields = ('nome',)
    list_filter = ('nivel',)

@admin.register(Formacao)
class FormacaoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'instituicao', 'data_inicio', 'data_fim')
    search_fields = ('nome', 'instituicao')
    list_filter = ('instituicao',)
    ordering = ('-data_inicio',)

@admin.register(TFC)
class TFCAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'ano', 'rating')
    search_fields = ('titulo', 'autor', 'orientador')
    list_filter = ('ano', 'rating')

@admin.register(ExperienciaProfissional)
class ExperienciaProfissionalAdmin(admin.ModelAdmin):
    list_display = ('empresa', 'cargo', 'tipo', 'data_inicio', 'data_fim', 'destaque')
    search_fields = ('empresa', 'cargo')
    list_filter = ('tipo', 'destaque')
    ordering = ('-data_inicio',)

@admin.register(MakingOf)
class MakingOfAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'entidade_relacionada', 'data_registo')
    search_fields = ('titulo', 'entidade_relacionada')
    list_filter = ('entidade_relacionada',)