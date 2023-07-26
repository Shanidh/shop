import sys
import requests
import traceback
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework import authentication, permissions
from rest_framework.authentication import SessionAuthentication
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model, authenticate, logout, login
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db import transaction
from shopapp.models import CustomUser, UserType, Product, Cart, Order, ProductRating
from django.shortcuts import render, redirect
from rest_framework.permissions import IsAuthenticated

from ..serializers import (
    CustomerSerializer,
    CreateCustomerSerializer,
    CustomerProductListSerializer,
    CustomerCartSerializer,
    CustomerOrderProductSerializer,
    CustomerOrderListSerializer,
)

from ..services import (
    create_customer,
    create_order,
)


class CustomerLoginAPI(APIView):
    """API for Admin Login."""

    authentication_classes = [SessionAuthentication]

    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None and user.user_type == UserType.CUSTOMER:
                # Login successful, return user data
                login(request, user)
                data = {
                   "Success": True,
                   "msg": "Login Success",
                }
                return Response(status=status.HTTP_201_CREATED, data=data)
                # return redirect("shopapp:customer_list") 
            else:
            # Login failed
                return Response({'error': 'Invalid login credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            # Invalid data
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 


class CustomerLogOutAPI(APIView):
    """API for Logout."""
    def get(self, request):
        logout(request)
        return redirect("shopapp:customer_login")  


class CustomerRegisterAPI(APIView):
    """API for creating User"""

    authentication_classes = [SessionAuthentication]

    def post(self, request):
        try:
            serializer = CreateCustomerSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            with transaction.atomic():
                create_customer(**serializer.validated_data)
            return Response(status=status.HTTP_201_CREATED, data=_("User created succesfully."))
        except ValidationError as e:
            mes = "\n".join(e.messages)
            raise ValidationError(mes)
        except Exception:
            error_info = "\n".join(traceback.format_exception(*sys.exc_info()))
            print(error_info)
            data = {
                "Success": False,
                "msg": "User Registration Failed",
            }
            return Response(status=status.HTTP_400_BAD_REQUEST, data=data)       


class CustomerProductListAPI(APIView):
    """API for getting Product list."""

    authentication_classes = [SessionAuthentication]

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        try:
            result = Product.objects.all().values("id", "name", "description", "price").order_by("-created_date")
            serializer = CustomerProductListSerializer(result, many=True)
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        except ValidationError as e:
            mes = "\n".join(e.messages)
            raise ValidationError(mes)
        except Exception:
            error_info = "\n".join(traceback.format_exception(*sys.exc_info()))
            print(error_info)
            data = {
                "Success": False,
                "msg": "List getting failed",
            }
            return Response(status=status.HTTP_400_BAD_REQUEST, data=data)  


class AddtoCartAPI(APIView):
    """API for adding to cart."""

    authentication_classes = [SessionAuthentication]

    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        product = Product.objects.get(pk=id)
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart.products.add(product)
        return Response({'message': 'Product added to cart'}) 


class CustomerCartViewAPI(APIView):
    """API for getting Cart list."""

    authentication_classes = [SessionAuthentication]

    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CustomerCartSerializer(cart)
        return Response(serializer.data)  


class CustomerOrderProductAPI(APIView):
    """API for creating order for Customer"""

    authentication_classes = [SessionAuthentication]

    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        try:
            serializer = CustomerOrderProductSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            with transaction.atomic():
                create_order(user=user, **serializer.validated_data)
                data = {
                    "Success": True,
                    "msg": "New order created.",
                }
            return Response(status=status.HTTP_200_OK, data=data)
        except ValidationError as e:
            mes = "\n".join(e.messages)
            raise ValidationError(mes)
        except Exception:
            error_info = "\n".join(traceback.format_exception(*sys.exc_info()))
            print(error_info)
            data = {
                "Success": False,
                "msg": "Creating order failed",
            }
            return Response(status=status.HTTP_400_BAD_REQUEST, data=data)     


class CustomerOrderListAPI(APIView):
    """API for getting order list."""

    authentication_classes = [SessionAuthentication]

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        try:
            result = Order.objects.filter(user=user).values("id", "product__name", "status", "quantity").order_by("-created_date")
            serializer = CustomerOrderListSerializer(result, many=True)
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        except ValidationError as e:
            mes = "\n".join(e.messages)
            raise ValidationError(mes)
        except Exception:
            error_info = "\n".join(traceback.format_exception(*sys.exc_info()))
            print(error_info)
            data = {
                "Success": False,
                "msg": "List getting failed",
            }
            return Response(status=status.HTTP_400_BAD_REQUEST, data=data)      


class CustomerProductReviewAPI(APIView):
    """API for product review."""

    authentication_classes = [SessionAuthentication]

    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        product = Product.objects.get(pk=id)
        rating = request.data.get('rating', 0)
        ProductRating.objects.create(user=request.user, product=product, rating=rating)
        return Response({'message': 'Product rated successfully'})                                     