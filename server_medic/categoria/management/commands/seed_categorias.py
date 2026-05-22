from django.core.management.base import BaseCommand
from server_medic.categoria.models import Categoria, TipoChoices, NivelChoices


class Command(BaseCommand):
    help = "Popula a tabela de categorias com todas as combinacoes tipo x nivel"

    def handle(self, *args, **options):
        criadas = 0
        for tipo in TipoChoices.values:
            for nivel in NivelChoices.values:
                _, created = Categoria.objects.get_or_create(
                    tipo=tipo, nivel_complexidade=nivel
                )
                if created:
                    criadas += 1
        self.stdout.write(self.style.SUCCESS(
            f"{criadas} categorias criadas (total: {Categoria.objects.count()})"
        ))
