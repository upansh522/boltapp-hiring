from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core import signing
from .serializers import UserRegisterSerializer, UserRecognizeSerializer, UserVerifySerializer
from .models import User


@api_view(['POST'])
def register(request):
    """User registration endpoint."""
    serializer = UserRegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.create()
        return Response({
            'success': True,
            'user': {
                'id': user.id,
                'email': user.email,
                'firstName': user.first_name,
                'lastName': user.last_name,
            },
            'code': user._plain_login_code,  # Return actual code for first-time display
            'message': 'Registration successful. 6-digit login code has been generated and stored securely.',
        }, status=status.HTTP_201_CREATED)
    return Response({
        'success': False,
        'message': 'Invalid data',
        'errors': serializer.errors,
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def recognize(request):
    """Check if user is registered by email."""
    email = request.query_params.get('email', '')
    serializer = UserRecognizeSerializer(data={'email': email})
    if serializer.is_valid():
        registered = serializer.validated_data.get('registered', False)
        user = serializer.validated_data.get('user')
        
        if registered and user:
            return Response({
                'success': True,
                'user': {
                    'id': user.id,
                },
                'registered': True,
            })
        else:
            return Response({
                'success': True,
                'registered': False,
            })
    return Response({
        'success': False,
        'message': 'Invalid email format.',
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def verify(request):
    """Verify login code OTP."""
    serializer = UserVerifySerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        checkout_auth_token = signing.dumps(
            {'user_id': user.id},
            salt='checkout-authentication',
        )
        return Response({
            'success': True,
            'user': {
                'id': user.id,
                'email': user.email,
                'firstName': user.first_name,
                'lastName': user.last_name,
            },
            'checkout_auth_token': checkout_auth_token,
        })
    return Response({
        'success': False,
        'message': serializer.errors.get('code', ['Invalid login code.'])[0],
    }, status=status.HTTP_400_BAD_REQUEST)
