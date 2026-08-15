from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import CheckoutSerializer
from .models import Checkout


@api_view(['POST'])
def create(request):
    """Create checkout entry - authenticated or guest with idempotency support."""
    serializer = CheckoutSerializer(data=request.data)
    if serializer.is_valid():
        # The serializer.save() handles idempotency logic
        # user is passed as None from the view for guest checkout
        checkout = serializer.save(user=None)
        
        # Determine the key to return
        idempotency_key = checkout.idempotency_key
        
        # Check if this was a duplicate request (existing checkout returned)
        # If the user provided an idempotency_key and an existing checkout was found,
        # the serializer would have returned the existing checkout already.
        # Otherwise, it's a new checkout.
        
        return Response({
            'success': True,
            'message': 'Checkout information saved successfully',
            'checkout_id': checkout.id,
            'user_id': checkout.user.id if checkout.user else None,
            'idempotency_key': str(idempotency_key),
        }, status=status.HTTP_201_CREATED)
    return Response({
        'success': False,
        'message': 'Invalid data',
        'errors': serializer.errors,
    }, status=status.HTTP_400_BAD_REQUEST)