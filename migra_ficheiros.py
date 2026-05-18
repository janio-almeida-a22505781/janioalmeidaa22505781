import os
from django.core.files import File
from escola.models import Curso   # adaptar ao modelo

for obj in Curso.objects.all():
    if obj.imagem and obj.imagem.name:   # adaptar o nome do campo (neste caso é "imagem")
        local_path = obj.imagem.path    # adequar

        if os.path.exists(local_path):
            with open(local_path, 'rb') as f:
                obj.imagem.save(                         # adequar
                    os.path.basename(local_path),
                    File(f),
                    save=True
                )
            print(f"Migrado: {obj}")
