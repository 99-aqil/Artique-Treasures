from rest_framework import serializers

from .models import User, Product


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'fullname', 
            'email', 
            'username', 
            'password', 
            'userType',
            'address_line1', 
            'address_line2', 
            'city', 
            'state', 
            'zip_code',
            'country'
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
            "status",
            "get_image",
            "get_thumbnail"
        ]