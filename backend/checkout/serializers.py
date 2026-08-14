from rest_framework import serializers
from .models import Checkout


class CheckoutSerializer(serializers.Serializer):
    """Serializer for checkout creation with idempotency support."""
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=20)
    shipping_address = serializers.CharField()
    idempotency_key = serializers.UUIDField(required=False, allow_null=True)

    def validate_idempotency_key(self, value):
        """Validate that idempotency key is a valid UUID."""
        if value is not None:
            try:
                uuid.UUID(value)
            except ValueError:
                raise serializers.ValidationError("Idempotency key must be a valid UUID.")
        return value

    def save(self, **kwargs):
        """Save and return a new checkout instance with idempotency."""
        validated_data = self.validated_data
        idempotency_key = validated_data.get('idempotency_key')
        user = kwargs.get('user')
        
        # Check for existing checkout with same idempotency key (idempotent behavior)
        existing_checkout = None
        if idempotency_key:
            try:
                existing_checkout = Checkout.objects.get(idempotency_key=idempotency_key)
            except Checkout.DoesNotExist:
                existing_checkout = None
        
        if existing_checkout:
            # Return existing checkout - idempotent behavior
            return existing_checkout
        
        # Use the provided idempotency key if available, otherwise generate a new one
        if idempotency_key:
            # Key was provided but doesn't exist in DB - use it anyway
            new_key = idempotency_key
        else:
            # No key provided - generate a new one
            import uuid
            new_key = uuid.uuid4()
        
        checkout = Checkout.objects.create(
            user=user,
            email=validated_data['email'],
            phone=validated_data['phone'],
            shipping_address=validated_data['shipping_address'],
            idempotency_key=new_key,
        )
        return checkout