from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models_organization import UserProfile, Organization

@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Associa o usuário à primeira organização existente, ou crie uma padrão
        organization = Organization.objects.first()
        if not organization:
            organization = Organization.objects.create(name='Padrão')
        UserProfile.objects.create(user=instance, organization=organization)
