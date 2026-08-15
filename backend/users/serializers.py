import bcrypt
from rest_framework import serializers
from .models import User


class UserRegisterSerializer(serializers.Serializer):
    """Serializer for user registration."""
    email = serializers.EmailField(max_length=255)
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)

    def validate_email(self, value):
        """Validate email format and check uniqueness."""
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        if not value or not value.strip():
            raise serializers.ValidationError("Email is required.")
        return value

    def create(self):
        """Create and return a new user instance."""
        # Use email as username since we're using email as USERNAME_FIELD
        username = self.validated_data['email'].split('@')[0]
        user = User.objects.create(
            username=username,
            email=self.validated_data['email'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
        )
        # Generate 6-digit login code and hash it
        import random
        login_code_plain = str(random.randint(100000, 999999))
        hashed_code = bcrypt.hashpw(login_code_plain.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        user.login_code = hashed_code
        user.save()
        # Attach plain code as temporary attribute for response
        user._plain_login_code = login_code_plain
        return user


class UserRecognizeSerializer(serializers.Serializer):
    """Serializer for user recognition (check if email is registered)."""
    email = serializers.EmailField()

    def validate(self, data):
        """Validate email format and check if user exists - single query."""
        email = data.get('email')
        if not email or not email.strip():
            raise serializers.ValidationError("Email is required.")

        # Single query to check user existence
        user = User.objects.filter(email__iexact=email).first()
        if not user:
            # Still set registered: false response format
            data['user'] = None
            data['registered'] = False
            return data
        
        data['user'] = user
        data['registered'] = True
        return data


class UserVerifySerializer(serializers.Serializer):
    """Serializer for OTP code verification."""
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)

    def validate(self, data):
        """Validate email and verified code match."""
        email = data.get('email')
        code = data.get('code')

        if not email or not code:
            raise serializers.ValidationError("Email and code are required.")

        if len(code) != 6 or not code.isdigit():
            raise serializers.ValidationError("Code must be exactly 6 digits.")

        try:
            user = User.objects.get(email__iexact=email)
            # Match with hashed code stored in DB
            if not bcrypt.checkpw(code.encode('utf-8'), user.login_code.encode('utf-8')):
                raise serializers.ValidationError("Invalid login code.")
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")

        data['user'] = user
        return data