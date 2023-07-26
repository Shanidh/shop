from django.db import models
from django.conf import settings
from shopapp.models import Product
from django.utils.translation import gettext_lazy as _


class OrderStatus(models.TextChoices):
    APPROVED = "APPROVED", _("Approved")
    SHIPPED = "SHIPPED", _("Shipped")
    DELIVERED = "DELIVERED", _("Delivered")


class Order(models.Model):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="order_user",
        null=True,
    )
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, related_name="products")
    status = models.CharField(
        help_text=_("Order Status"),
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.APPROVED,
        null=True,
        )
    quantity = models.PositiveIntegerField(default=1)
    created_date = models.DateTimeField(auto_now_add=True, null=True)