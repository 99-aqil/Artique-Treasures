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
                all_users = User.objects.all()
                all_users_serializer = UserSerializer(all_users, many=True)
                return Response({'message': 'Seller', 'data': all_users_serializer.data}, status=status.HTTP_201_CREATED)
                # return render(request, 'sellerView.html', {'users': all_users_serializer.data})
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            # return render(request, 'customerView.html', {'user': serializer.data})
        except User.DoesNotExist:
            return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)


"""***************************************** APIS  FOR  SELLER *****************************************"""
            

class ProductsListSellerView(APIView):
    def get(self, request, format=None):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return render(request, 'sellerView.html', {'latestProducts': serializer.data})
        # return Response(serializer.data)


"""***************************************** APIS  FOR  Customer *****************************************"""


class ProductsListCustomerView(APIView):
    def get(self, request, format=None):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return render(request, 'customerView.html', {'latestProducts': serializer.data})
        # return Response(serializer.data)


class ArtCategoryView(APIView):
    def get(self, request):
        products = Product.objects.filter(category="Art")
        serializer = ProductSerializer(products, many=True)
        return render(request, 'art.html', {'products': serializer.data})


class AntiqueCategoryView(APIView):
    def get(self, request):
        products = Product.objects.filter(category="Antique")
        serializer = ProductSerializer(products, many=True)
        return render(request, 'antique.html', {'products': serializer.data})
        

class ProductDetailAPI(APIView):
    def get(self, request, pk=None):
        if pk:
            try:
                instance = Product.objects.get(pk=pk)
                serializer = ProductSerializer(instance)
                return render(request, 'productDetail.html', {'product': serializer.data})
                # return Response(serializer.data)
            except Product.DoesNotExist:
                return Response({"error": "Object not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            queryset = Product.objects.all()
            serializer = ProductSerializer(queryset, many=True)
            return Response(serializer.data)
            

@api_view(['GET', 'POST'])
def search(request):
    query = request.GET.get('query', '')

    if query:
        products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        serializer = ProductSerializer(products, many=True)
        return render(request, 'search.html', {'products': serializer.data, 'query': query})
    else:
        return render(request, 'search.html', {'products': [], 'query': query})