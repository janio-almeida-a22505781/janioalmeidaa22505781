from django.db import models

# Create your models here.

class Licenciatura(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField()
    duracao_anos = models.IntegerField()
    universidade = models.CharField(max_length=200)
    link = models.URLField()

    def __str__(self):
        return self.nome
    
class UnidadeCurricular(models.Model):
    nome = models.CharField(max_length=200)
    codigo = models.CharField(max_length=50)
    descricao = models.TextField()

    ano = models.IntegerField()
    semestre = models.IntegerField()

    # By API
    ects = models.FloatField(default=0)
    horas_contacto = models.IntegerField(default=0)

    docente = models.CharField(max_length=200)
    link_docente = models.URLField()

    imagem = models.ImageField(upload_to='ucs/')

    licenciatura = models.ForeignKey(
        Licenciatura,
        on_delete=models.CASCADE,
        related_name='ucs'
    )
    
class Tecnologia(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()

    website = models.URLField()
    logo = models.ImageField(upload_to='tecnologias/')

    nivel = models.IntegerField(help_text="Nível de 1 a 5")

    def __str__(self):
        return self.nome
    
class Projeto(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField()
    
    conceitos_aplicados = models.TextField()
    
    github_link = models.URLField()
    demo_video = models.URLField(blank=True, null=True)

    imagem = models.ImageField(upload_to='projetos/')

    data_criacao = models.DateField()

    unidade_curricular = models.ForeignKey(
        UnidadeCurricular,
        on_delete=models.CASCADE,
        related_name='projetos'
    )

    tecnologias = models.ManyToManyField(
        Tecnologia,
        related_name='projetos',
        blank=True
    )
    def __str__(self):
        return self.nome
    
class Competencia(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    
    nivel = models.IntegerField(help_text="Nível de 1 a 5")
    
    tecnologias = models.ManyToManyField(
        Tecnologia,
        related_name='competencias',
        blank=True
    )

    def __str__(self):
        return self.nome
    
class Formacao(models.Model):
    nome = models.CharField(max_length=200)
    instituicao = models.CharField(max_length=200)
    
    data_inicio = models.DateField()
    data_fim = models.DateField(blank=True, null=True)
    
    descricao = models.TextField(blank=True)

    def __str__(self):
        return f"{self.nome} - {self.instituicao}"
    
class TFC(models.Model):
    titulo = models.CharField(max_length=300)
    autor = models.CharField(max_length=200)
    orientador = models.TextField()
    
    curso = models.CharField(max_length=200)
    ano = models.IntegerField()

    resumo = models.TextField(blank=True)

    palavras_chave = models.TextField(blank=True)
    areas = models.TextField(blank=True)
    tecnologias = models.TextField(blank=True)

    email = models.EmailField(blank=True)
    
    imagem = models.URLField(blank=True)
    pdf = models.URLField(blank=True)

    rating = models.IntegerField()

    def __str__(self):
        return self.titulo
    
class ExperienciaProfissional(models.Model):
    empresa = models.CharField(max_length=200)
    cargo = models.CharField(max_length=200)
    
    tipo = models.CharField(
        max_length=50,
        choices=[
            ('estagio', 'Estágio'),
            ('part_time', 'Part-time'),
            ('full_time', 'Full-time'),
        ]
    )

    localizacao = models.CharField(max_length=200)
    
    data_inicio = models.DateField()
    data_fim = models.DateField(blank=True, null=True)

    descricao = models.TextField()

    tecnologias = models.ManyToManyField(
        Tecnologia,
        related_name='experiencias',
        blank=True
    )

    destaque = models.BooleanField(
        default=False,
        help_text="Marcar experiências mais importantes"
    )

    def __str__(self):
        return f"{self.cargo} - {self.empresa}"
    
class MakingOf(models.Model):

    titulo = models.CharField(max_length=200)

    entidade_relacionada = models.CharField(
        max_length=100,
        help_text="Ex: Projeto, UC, Tecnologia, TFC, etc."
    )

    descricao_decisoes = models.TextField()

    erros_encontrados = models.TextField(blank=True)

    correcoes_aplicadas = models.TextField(blank=True)

    justificacao_modelacao = models.TextField()

    uso_ia = models.TextField(
        blank=True,
        help_text="Descrição do uso de IA no desenvolvimento"
    )

    data_registo = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo