from shopapp.models import CustomUser, UserType
from django.contrib.auth import get_user_model
from ..models import Order, OrderStatus

User = get_user_model()


def create_customer(
    username: str,
    password: str,
) -> None:
    user = CustomUser.objects.create_user(username=username, password=password, user_type=UserType.CUSTOMER)


def create_order(
    user: User,
    product_id: str,
) -> None:
    order = Order(
        product_id=product_id,
        user=user,
    )
    if Order(product_id=product_id, user=user, status=OrderStatus.APPROVED).exists():
        orders = Order.objects.get(product_id=product_id, user=user, status=OrderStatus.APPROVED)
        quantity = int(orders.quantity)
        orders.quantity = quantity+1
        orders.save()
    order.save()      