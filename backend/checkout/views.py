from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import CheckoutSerializer
from .models import Checkout
from django.contrib.auth import get_user_model


@api_view(['POST'])
def create(request):
    """Create checkout entry - authenticated or guest."""
    serializer = CheckoutSerializer(data=request.data)
    if serializer.is_valid():
        user = None
        # Check if user is authenticated via JWT or session
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        User = get_user_model()
        
        if auth_header.startswith('Bearer '):
            token = auth_header[7:]
            try:
                user_obj = User.objects.get(login_code=token)
                if user_obj:
                    user = user_obj
            except User.DoesNotExist:
                pass
        
        checkout = serializer.save(user=user)
        return Response({
            'success': True,
            'message': 'Checkout information saved successfully',
            'checkout_id': checkout.id,
            'user_id': checkout.user.id if checkout.user else None,
        }, status=status.HTTP_201_CREATED)
    return Response({
        'success': False,
        'message': 'Invalid data',
        'errors': serializer.errors,
    }, status=status.HTTP_400_BAD_REQUEST)