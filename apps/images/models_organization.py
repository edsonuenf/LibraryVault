from django.db import models
from django.contrib.auth import get_user_model

class Organization(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # Outros campos relevantes para SaaS podem ser adicionados aqui

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    # Outros campos de perfil podem ser adicionados aqui

    def __str__(self):
        return f"{self.user.username} ({self.organization.name})"
