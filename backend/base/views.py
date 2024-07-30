from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from . models import Profile
from .forms import UserRegistrationForm

@api_view(['POST'])
def register(request):
    form = UserRegistrationForm(request.data)
    print('data' , request.data)
    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        Profile.objects.create(user = user)
        
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)