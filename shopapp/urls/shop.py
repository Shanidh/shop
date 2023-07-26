from django.urls import path
from ..apis import shop


urlpatterns = [
  path("", shop.LoginAPI.as_view(), name="login"), 
  path("logout", shop.LogOutAPI.as_view(), name="logout"),
  path("customer/list", shop.CustomerListAPI.as_view(), name="customer_list"),
  path("product/create", shop.CreateProductAPI.as_view(), name="product_create"),
  path('product/delete/<int:id>', shop.DeleteProductAPI.as_view(), name="product_delete"),
  path('product/update/<int:id>', shop.UpdateProductAPI.as_view(), name="product_update"),
  path('order/list', shop.OrderListAPI.as_view(), name="order_list"),
  path('change/orderstatus', shop.ChangeOrderStatusAPI.as_view(), name="change_order_status"),
  path("product/list", shop.ProductListAPI.as_view(), name="product_list"),
]