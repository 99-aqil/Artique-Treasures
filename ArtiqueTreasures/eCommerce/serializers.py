from rest_framework import serializers

from .models import User, Product


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'fullname', 
            'email', 
            'username', 
            'password', 
            'userType'
            ]

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "category",
            "name",
            "description",
            "price",
            "get_image",
            "get_thumbnail"
        ]