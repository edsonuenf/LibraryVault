from django.db import models

class GlobalSettings(models.Model):
    items_per_page = models.PositiveIntegerField(default=15, verbose_name="Itens por página")
    pagination_visible_pages = models.PositiveIntegerField(default=5, verbose_name="Páginas visíveis na paginação")

    def __str__(self):
        return "Configurações Globais"

    class Meta:
        verbose_name = "Configuração Global"
        verbose_name_plural = "Configurações Globais"
