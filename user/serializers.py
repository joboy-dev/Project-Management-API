from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class CreateAccountSerializer(serializers.ModelSerializer):
    ''' Serializer to create new user '''

    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'password', 'password2', 'profile_pic', 'phone_number', 'subscription_plan', 'is_verified']
        read_only_fields = ['id', 'is_verified']        
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        '''Account creation validation function'''

        # validate password
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'error': 'Your passwords do not match'})
        
        # validate subscription plan
        if data['subscription_plan'] not in ['basic', 'premium', 'enterprise']:
            raise serializers.ValidationError({'error': 'This subscription plan is not available. Choose between basic, premium, and enterprise'})
        
        # check if email exists
        elif User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({'error': 'Email already exists'})
        
        # validate password
        validate_password(data['password'])
        # return validated data
        return data
    
    def create(self, validated_data):
        '''Account creation function'''
        
        # password = validated_data.pop('password', None)
        # user = self.create_user(password=password, **validated_data)

        # return user

        # get all validated data
        email = validated_data.get('email')
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        password = validated_data.get('password')
        profile_pic = validated_data.get('profile_pic')
        phone_number = validated_data.get('phone_number')
        subscription_plan = validated_data.get('subscription_plan')

        # assign validated data to the data in User model
        account = User(
            email=email, 
            first_name=first_name, 
            last_name=last_name,
            profile_pic=profile_pic,
            phone_number=phone_number,
            subscription_plan=subscription_plan,
        )

        # set password
        account.set_password(raw_password=password)

        # save user instance
        account.save()

        return account
    

class ResendEmailVerificationSerializer(serializers.Serializer):
    '''Serializer to resend email verifiaction'''
    
    email = serializers.EmailField(required=True)
        
    def validate(self, data):
        if not User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({'error': 'This user does not exist'})
        
        return data
        
    

class LoginSerializer(serializers.Serializer):

    '''Serializer to log in a user.'''

    # declare fields to use for the serializer
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    
    def validate(self, data):
        '''Authentication validation function'''

        # authenticate user with email and password
        user = authenticate(email=data['email'], password=data['password'])

        # check for existence of user
        if user is None:
            raise serializers.ValidationError({'error': 'User does not exist'})
        
        # check if user is verified
        elif not user.is_verified:
            raise serializers.ValidationError({'error': 'Email is not verified'})
        
        elif not user.is_active:
            raise serializers.ValidationError({'error': 'This user is not active'})
        
        # remove fields from dictionary that you don't want to see in JSON response
        email = data.pop('email')
        data.pop('password')

        # create token for jwt
        refresh_token = RefreshToken.for_user(user=user)
        
        data['message'] = f'Welcome {email}'
        data['token'] = {
            'refresh': str(refresh_token),
            'access': str(refresh_token.access_token)
        }

        return data

    
class UserDetailsSerializer(serializers.ModelSerializer):

    '''Serializer to update a user's details.'''

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'profile_pic', 'phone_number', 'is_verified']
        read_only_fields = ['id', 'is_verified']        
    
    def update(self, instance, validated_data):
        '''Update details function'''

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance
    

class ChangePasswordSerializer(serializers.Serializer):
    '''Serializer to change user password.'''

    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)
    
    def update(self, instance, validated_data):
        email = validated_data.get('email')
        old_password = validated_data.get('password')
        new_password = validated_data.get('new_password')
        confirm_password = validated_data.get('confirm_password')

        user = authenticate(email=email, password=old_password)

        if user is None:
            raise serializers.ValidationError({'error': 'User credentials incorrect. Check your email and password and try again.'})
        elif old_password == new_password:
            raise serializers.ValidationError({'error': 'New password cannot be the same as old password.'})
        elif new_password != confirm_password:
            raise serializers.ValidationError({'error': 'New password and confirm password field has to be the same.'})
        
        validate_password(new_password)
        instance.set_password(new_password)

        instance.save()

        return instance
    

class ChangeEmailSerializer(serializers.Serializer):
    '''Serializer to change user email'''
    
    email = serializers.EmailField(required=True)
    
    def validate(self, data):
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({'error': 'This email already exists'})
        
        return data
    
    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
            
        instance.save()
        return instance
    

class UpdateSubscriptionPlanSerializer(serializers.ModelSerializer):
    '''Serializer to update subscription plan.'''
    
    class Meta:
        model = User
        fields = ['id', 'subscription_plan']
        extra_kwargs = {
            'id': {'read_only': True},
        }
        
    def validate(self, data):
         # validate subscription plan
        if data['subscription_plan'] not in ['basic', 'premium', 'enterprise']:
            raise serializers.ValidationError({'error': 'This subscription plan is not available. Choose between basic, premium, and enterprise'})
    
    def update(self, instance, validated_data):
        
        for key, value in validated_data.items():
            setattr(instance, key, value)
            
        instance.save()
        return instance
    
    