from rest_framework import routers
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from api.views import PostModelViewSet, UserModelViewSet

router = routers.DefaultRouter()
router.register(r'users', UserModelViewSet)
router.register(r'posts', PostModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token-auth/', obtain_auth_token, name='token-auth'),
    path('auth/', include('rest_framework.urls',
         namespace='rest_framework'), name='basic-auth'),
]
