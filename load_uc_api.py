import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

import requests
from portfolio.models import UnidadeCurricular, Licenciatura

URL = "https://secure.ensinolusofona.pt/dados-publicos-academicos/resources/GetCourseDetail"

payload = {
    "language": "PT",
    "courseCode": 260,
    "schoolYear": "202526"
}

headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0"
}


def map_semestre(semester_code):
    if semester_code == "S":
        return 1  # anual / semestral genérico
    elif semester_code == "1":
        return 1
    elif semester_code == "2":
        return 2
    return 1


def run():
    print("🔍 A obter dados do curso...")

    try:
        response = requests.post(URL, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"❌ Erro: {e}")
        return

    ucs = data.get("courseFlatPlan", [])
    print(f"📚 {len(ucs)} UCs encontradas")

    licenciatura = Licenciatura.objects.first()

    for uc in ucs:
        try:
            nome = uc.get("curricularUnitName")
            codigo = uc.get("curricularIUnitReadableCode")
            ano = uc.get("curricularYear")
            semestre = map_semestre(uc.get("semesterCode"))

            ects = uc.get("ects", 0)
            horas = uc.get("hrTotalContactoInt", 0)

            UnidadeCurricular.objects.update_or_create(
                codigo=codigo,
                defaults={
                    "nome": nome,
                    "descricao": "Descrição não disponível (API)",
                    "ano": ano,
                    "semestre": semestre,
                    "ects": ects,
                    "horas_contacto": int(horas),

                    # 👇 campos obrigatórios preenchidos manualmente
                    "docente": "Não definido",
                    "link_docente": "https://www.ulusofona.pt",
                    "imagem": "ucs/default.png",

                    "licenciatura": licenciatura
                }
            )

            print(f"✅ {nome}")

        except Exception as e:
            print(f"⚠️ Erro ao salvar UC: {e}")

    print("🎉 Importação concluída!")