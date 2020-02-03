from django.dispatch import receiver
from django.core.signals import post_save
from .models import *

@receiver(post_save, sender=Product)
def create_product(sender, instance, created, **kwargs):
    if created:
        Hit.objects.create(product=instance)
        