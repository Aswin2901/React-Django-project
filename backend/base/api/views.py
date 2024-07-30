from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view , permission_classes
from rest_framework.permissions import IsAuthenticated , IsAdminUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import ProfileSerializer , UserSerializer
from base.models import Profile

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        # ...

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['GET'])
def getRoutes(request):
    routes =[
        '/api/token',
        '/api/token/refresh',
    ]
    
    return Response(routes)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getProfile(request):
    user = request.user
    profile = Profile.objects.filter(user = user)
    serializer = ProfileSerializer(profile , many= True)
    
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUser(request):
    user = request.user
    serializer = UserSerializer(user)
    
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_profile_pic(request):
    if 'profile_pic' in request.FILES:
        profile_pic = request.FILES['profile_pic']
        profile = Profile.objects.get(user=request.user)
        profile.profile_pic = profile_pic
        profile.save()
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)
    else:
        return Response({'error': 'No profile picture provided'}, status=400)
    
@api_view(['GET'])
@permission_classes([IsAdminUser])
def adminGetUser(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    
    return Response(serializer.data)

@api_view(['POST'])  
@permission_classes([IsAdminUser])
def adminRemoveUser(request):
    user_id = request.data.get('user_id')

    try:
        user = User.objects.get(pk=user_id)
        user.delete()
        return Response("User removed successfully", status=status.HTTP_204_NO_CONTENT)
    except User.DoesNotExist:
        return Response("User not found", status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST'])
@permission_classes([IsAdminUser])
def adminEditUser(request):
    user_id = request.data.get('user_id')
    if not user_id:
        return Response({'error': 'User ID is required'}, status=400)

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)

    if 'username' in request.data:
        user.username = request.data['username']

    if 'email' in request.data:
        new_email = request.data['email']
        if User.objects.filter(email=new_email).exclude(id=user_id).exists():
            return Response({'error': 'Email is already in use by another user'}, status=400)
        user.email = new_email

    if 'first_name' in request.data:
        user.first_name = request.data['first_name']
    if 'last_name' in request.data:
        user.last_name = request.data['last_name']

    user.save()

    return Response({'message': 'User updated successfully'})