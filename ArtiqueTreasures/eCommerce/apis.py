from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import authenticate

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated

from .serializers import UserSerializer, ProductSerializer
from .models import User, Product


"""***************************************** LOGIN AND REGISTRATION *****************************************"""

class UserRegistrationAPIView(APIView):
    
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            # return redirect('login-page')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        try:
            user = User.objects.get(username=username, password=password)
            if user.userType == 'Seller':
                user_serializer = UserSerializer(user)
                return Response({'message': 'Seller', 'user': user_serializer.data}, status=status.HTTP_201_CREATED)
                # return render(request, 'sellerView.html', {'users': all_users_serializer.data})
            elif user.userType == 'Admin':
                user_serializer = UserSerializer(user)
                return Response({'message': 'Admin', 'user': user_serializer.data}, status=status.HTTP_201_CREATED)
                # return render(request, 'sellerView.html', {'users': all_users_serializer.data})
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            # return render(request, 'customerView.html', {'user': serializer.data})
        except User.DoesNotExist:
            return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)


"""***************************************** APIS  FOR  ADMIN *****************************************"""
            

class AdminViewAPI(APIView):
    def get(self, request):
        users = User.objects.all()
        user_serializer = UserSerializer(users, many=True)
        products = Product.objects.all()
        product_serializer = ProductSerializer(products, many=True)
        return render(request, 'adminView.html', {'users': user_serializer.data, 'latestProducts': product_serializer.data})
        # return Response(serializer.data)


"""***************************************** APIS  FOR  SELLER *****************************************"""
            

class SellerViewAPI(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return render(request, 'sellerView.html', {'latestProducts': serializer.data})
        # return Response(serializer.data)


"""***************************************** APIS  FOR  Customer *****************************************"""

class CustomerViewAPI(APIView):
    def get(self, request, format=None, pk=None):
        user = User.objects.get(pk=pk)
        user_serializer = UserSerializer(user)
        products = Product.objects.filter(status__in=["Approved", "Order Placed", "Dispatched"])
        product_serializer = ProductSerializer(products, many=True)
        return render(request, 'customerView.html', {'user': user_serializer.data, 'latestProducts': product_serializer.data})
        # response_data = {"user": user_serializer.data, "product": product_serializer.data}
        # return Response(response_data)

class CustomerInfoAPI(APIView):
    def get(self, request, pk=None):
        if pk:
            try:
                instance = User.objects.get(pk=pk)
                serializer = UserSerializer(instance)
                return render(request, 'myInfo.html', {'user': serializer.data})
                # return Response(serializer.data)
            except Product.DoesNotExist:
                return Response({"error": "Object not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            queryset = User.objects.all()
            serializer = UserSerializer(queryset, many=True)
            return Response(serializer.data)
    
    # def post(self, request, pk=None):
    #     if pk:
    #         instance = User.objects.get(pk=pk)
    #         serializer = UserSerializer(instance, data=request.data)
    #         if serializer.is_valid():
    #             serializer.save()
    #             return render(request, 'myInfo.html', {'user': serializer.data})
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ArtCategoryView(APIView):
    def get(self, request, pk=None):
        user = User.objects.get(pk=pk)
        user_serializer = UserSerializer(user)
        products = Product.objects.filter(category="Art", status__in=["Approved", "Order Placed", "Dispatched"])
        serializer = ProductSerializer(products, many=True)
        return render(request, 'art.html', {'user': user_serializer.data, 'products': serializer.data})


# class AntiqueCategoryView(APIView):
#     def get(self, request, pk=None):
#         user = User.objects.get(pk=pk)
#         user_serializer = UserSerializer(user)
#         products = Product.objects.filter(category="Antique", status__in=["Approved", "Order Placed", "Dispatched"])
#         serializer = ProductSerializer(products, many=True)
#         return render(request, 'antique.html', {'user': user_serializer.data, 'products': serializer.data})
        

class ProductDetailAPI(APIView):
    def get(self, request, product_id=None, user_id=None):
        if product_id and user_id:
            try:
                user = User.objects.get(pk=user_id)
                user_serializer = UserSerializer(user)
                instance = Product.objects.get(pk=product_id)
                serializer = ProductSerializer(instance)
                return render(request, 'productDetail.html', {'user': user_serializer.data, 'product': serializer.data})
                # return Response(serializer.data)
            except Product.DoesNotExist:
                return Response({"error": "Object not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            queryset = Product.objects.all()
            serializer = ProductSerializer(queryset, many=True)
            return Response(serializer.data)
            

@api_view(['GET', 'POST'])
def search(request, pk=None):
    query = request.GET.get('query', '')
    user = User.objects.get(pk=pk)
    user_serializer = UserSerializer(user)

    if query:
        products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query), status__in=["Approved", "Order Placed", "Dispatched"])
        serializer = ProductSerializer(products, many=True)
        return render(request, 'search.html', {'user': user_serializer.data, 'products': serializer.data, 'query': query})
    else:
        return render(request, 'search.html', {'user': user_serializer.data, 'products': [], 'query': query})