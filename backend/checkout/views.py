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
        # Save with idempotency logic - serializer handles key generation/checking
        checkout = serializer.save(user=None)
        
        # Determine the key to return
        idempotency_key = checkout.idempotency_key
        
        # Check if this was a duplicate request (existing checkout returned)
        # The serializer returns the existing checkout if key already existed
        if checkout.idempotency_key and request.data.get('idempotency_key'):
            # This means an existing checkout was found and returned
            return Response({
                'success': True,
                'message': 'Checkout information retrieved successfully (idempotent)',
                'checkout_id': checkout.id,
                'user_id': checkout.user.id if checkout.user else None,
                'idempotency_key': str(checkout.idempotency_key),
            }, status=status.HTTP_200_OK)
        else:
            # New checkout created
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