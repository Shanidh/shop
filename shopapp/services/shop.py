from django.contrib.auth import get_user_model
from ..models import Product, Order, OrderStatus
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

User = get_user_model()


def create_product(
    user: User,
    name: str,
    description: str,
    price: str,
) -> None:
    product = Product(
        name=name,
        description=description,
        price=price,
    )
    product.save()    


def change_order_status(user: User, id: int) -> str:
    order = Order.objects.get(pk=id)
    if not order.status == OrderStatus.DELIVERED:
        if order.status == OrderStatus.SHIPPED:
            order.status = OrderStatus.DELIVERED
            order.save()
            return _("Order Delivered")
        else:
            order.status = OrderStatus.SHIPPED
            order.save()
            return _("Order Shipped")
    else:
        raise ValidationError(_("Order Already Delivered"))    