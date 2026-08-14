from rest_framework import serializers
from .models import Checkout


class CheckoutSerializer(serializers.Serializer):
    """Serializer for checkout creation."""
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=20)
    shipping_address = serializers.CharField()

    def save(self, **kwargs):
        """Save and return a new checkout instance."""
        validated_data = self.validated_data
        user = kwargs.get('user')
        checkout = Checkout.objects.create(
            user=user,
            email=validated_data['email'],
            phone=validated_data['phone'],
            shipping_address=validated_data['shipping_address'],
        )
        return checkout