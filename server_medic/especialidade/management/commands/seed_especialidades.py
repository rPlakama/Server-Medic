from django.core.management.base import BaseCommand
from server_medic.especialidade.models import Especialidade

ESPECIALIDADES = [
    "Acupuntura",
    "Alergia e Imunologia",
    "Anestesiologia",
    "Angiologia",
    "Cardiologia",
    "Cirurgia Cardiovascular",
    "Cirurgia da Mao",
    "Cirurgia de Cabeca e Pescoco",
    "Cirurgia do Aparelho Digestivo",
    "Cirurgia Geral",
    "Cirurgia Oncologica",
    "Cirurgia Pediatrica",
    "Cirurgia Plastica",
    "Cirurgia Toracica",
    "Cirurgia Vascular",
    "Clinica Medica",
    "Coloproctologia",
    "Dermatologia",
    "Endocrinologia e Metabologia",
    "Endoscopia",
    "Gastroenterologia",
    "Genetica Medica",
    "Geriatria",
    "Ginecologia e Obstetricia",
    "Hematologia e Hemoterapia",
    "Homeopatia",
    "Infectologia",
    "Mastologia",
    "Medicina de Emergencia",
    "Medicina de Familia e Comunidade",
    "Medicina do Trabalho",
    "Medicina do Trafego",
    "Medicina Esportiva",
    "Medicina Fisica e Reabilitacao",
    "Medicina Intensiva",
    "Medicina Legal e Pericia Medica",
    "Medicina Nuclear",
    "Medicina Preventiva e Social",
    "Nefrologia",
    "Neurocirurgia",
    "Neurologia",
    "Nutrologia",
    "Oftalmologia",
    "Oncologia Clinica",
    "Ortopedia e Traumatologia",
    "Otorrinolaringologia",
    "Patologia",
    "Patologia Clinica / Medicina Laboratorial",
    "Pediatria",
    "Pneumologia",
    "Psiquiatria",
    "Radiologia e Diagnostico por Imagem",
    "Radioterapia",
    "Reumatologia",
    "Urologia",
]


class Command(BaseCommand):
    help = "Popula a tabela de especialidades medicas"

    def handle(self, *args, **options):
        criadas = 0
        for nome in ESPECIALIDADES:
            _, created = Especialidade.objects.get_or_create(nome=nome)
            if created:
                criadas += 1
        self.stdout.write(self.style.SUCCESS(f"{criadas} especialidades criadas (total: {Especialidade.objects.count()})"))
