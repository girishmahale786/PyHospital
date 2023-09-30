from main.models import Employee, Post
from rest_framework import viewsets, status, mixins
from api.serializers import EmployeeSerializer, PostSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

# Create your views here.


class UserModelViewSet(mixins.CreateModelMixin,
                       mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       viewsets.GenericViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [AllowAny]

    def list(self, request):
        if request.user.is_authenticated:
            user = Employee.objects.get(user=request.user)
            return Response(EmployeeSerializer(user).data, status.HTTP_200_OK)
        else:
            return Response({"detail": "Authentication credentials were not provided."}, status.HTTP_401_UNAUTHORIZED)

    def retrieve(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().retrieve(request, *args, **kwargs)
        else:
            return Response({"detail": "Authentication credentials were not provided."}, status.HTTP_401_UNAUTHORIZED)


class PostModelViewSet(viewsets.ModelViewSet):
    lookup_field = 'slug'
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_queryset(self):
        queryset = Post.objects.all().order_by('-date', '-id')
        category = self.request.query_params.get('category')
        if category is not None:
            queryset = queryset.filter(
                category=category).order_by('-date', '-id')
        return queryset

    def create(self, request):
        data = request.data.copy()
        data['author'] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
