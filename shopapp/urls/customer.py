from django.urls import path
from ..apis import customer


urlpatterns = [
    path("login", customer.CustomerLoginAPI.as_view(), name="customer_login"),
    path("logout", customer.CustomerLogOutAPI.as_view(), name="customer_logout"),
    path("register", customer.CustomerRegisterAPI.as_view(), name="customer_register"),
    path("product/list", customer.CustomerProductListAPI.as_view(), name="customer_productlist"),
    path("addtocart/<int:id>", customer.AddtoCartAPI.as_view(), name="addtocart"),
    path("cart/view", customer.CustomerCartViewAPI.as_view(), name="viewcart"),
    path("order/product", customer.CustomerOrderProductAPI.as_view(), name="orderproduct"),
    path("order/list", customer.CustomerOrderListAPI.as_view(), name="orderlist"),
    path("product/review/<int:id>", customer.CustomerProductReviewAPI.as_view(), name="product_review"),
]