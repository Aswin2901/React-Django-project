from django.urls import path
from  . import views
from .views import MyTokenObtainPairView  , getProfile , upload_profile_pic , getUser , adminGetUser, adminRemoveUser, adminEditUser
from base.views import register
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('' , views.getRoutes),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', register, name='register'),
    path('profile/' , getProfile , name='profile' ),
    path('uploadProfile/' , upload_profile_pic , name='uploadProfile' ),
    path('getuser/' , getUser , name='getuser'),
    path('admingetuser/' , adminGetUser , name='admingetuser'),
    path('adminremoveuser/' , adminRemoveUser , name='adminremoveuser'),
    path('adminedituser/' , adminEditUser , name='adminedituser'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
