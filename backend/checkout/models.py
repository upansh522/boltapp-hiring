from django.db import models
from django.conf import settings


class Checkout(models.Model):
    """Checkout model for authenticated and guest checkouts."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='checkouts'
    )
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    shipping_address = models.TextField()
    idempotency_key = models.UUIDField(unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'checkouts'
        verbose_name = 'checkout'
        verbose_name_plural = 'checkouts'

    def __str__(self):
        return f"Checkout {self.id} - {self.email}"