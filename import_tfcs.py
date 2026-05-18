import os
import django
import json

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from portfolio.models import TFC

# Caminho do ficheiro JSON
with open('data/tfcs_2024_2025_full.json', encoding='utf-8') as f:
    data = json.load(f)

print(f"{len(data)} TFCs encontrados no JSON")

# Inserir na base de dados
for item in data:
    tfc = TFC.objects.create(
        titulo=item.get('titulo', ''),
        autor=item.get('autor', ''),
        orientador=item.get('orientador', ''),
        curso=item.get('curso', ''),
        ano=int(item.get('ano', 0)) if item.get('ano') else 0,
        resumo=item.get('resumo', ''),
        palavras_chave=", ".join(item.get('palavras_chave', [])),
        areas=", ".join(item.get('areas', [])),
        tecnologias=", ".join(item.get('tecnologias', [])),
        email=item.get('email', ''),
        imagem=item.get('imagem', ''),
        pdf=item.get('pdf', ''),
        rating=item.get('rating', 0)
    )

print("Importação concluída com sucesso!")