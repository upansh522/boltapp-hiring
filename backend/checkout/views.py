from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.core import signing
from .serializers import CheckoutSerializer
from .models import Checkout
from users.models import User


def authenticated_user_from_request(request):
    """Return the OTP-verified user encoded in a signed Bearer token, if present."""
    authorization = request.headers.get('Authorization', '')
    if not authorization.startswith('Bearer '):
        return None

    token = authorization.removeprefix('Bearer ').strip()
    try:
        payload = signing.loads(
            token,
            salt='checkout-authentication',
            max_age=settings.CHECKOUT_AUTH_TOKEN_MAX_AGE,
        )
        return User.objects.filter(id=payload.get('user_id')).first()
    except (signing.BadSignature, signing.SignatureExpired):
        return None


@api_view(['POST'])
def create(request):
    """Create checkout entry - authenticated or guest with idempotency support."""
    serializer = CheckoutSerializer(data=request.data)
    if serializer.is_valid():
        # A missing/invalid token intentionally keeps the checkout as a guest checkout.
        checkout = serializer.save(user=authenticated_user_from_request(request))
        
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
