from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import viewsets
from Myapp.models import Profile,Categroy, Blog, Comment
from django.contrib.auth.models import User
from rest_framework.reverse import reverse
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly, IsAuthenticated
from .permissions import IsAuthorOrReadOnly, IsUserOrReadOnly, IsAdminOrReadOnly
from .serializers import ( UserProfileSerializer,
                         UserCreateSerializer,
                          UserUpdateSerializer,
                          BlogSerializer,
                          CategroySerializer,
                          CommentSerializer,
                          CommentDetailsSerializer
                        )               


class ApiRoots(generics.GenericAPIView):
    def get(self, request):
        return Response(
            {
                'users':reverse('user-list', request = request),
                'profiles':reverse('profile-list', request = request),
                'categories':reverse('categroy-list', request = request),
                "blogs":reverse('blog-list', request = request),
                "comments":reverse('comment-list', request = request)
            }
        )


class UserRegisterApiView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer

class UserDetailsApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [IsUserOrReadOnly]

class UserProfilelistView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = UserProfileSerializer

class UserProfileDetailsView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthorOrReadOnly]
    def perform_update(self, serializer):
        serializer.save(author = self.request.user)


class CategroyListView(generics.ListCreateAPIView):
    serializer_class = CategroySerializer
    queryset = Categroy.objects.all()
    permission_classes = [IsAdminOrReadOnly]

class CategroyDetailsView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategroySerializer
    queryset = Categroy.objects.all()
    permission_classes = [IsAdminOrReadOnly]

class BlogListView(generics.ListCreateAPIView):
    serializer_class = BlogSerializer
    queryset = Blog.objects.all().order_by('-date')
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author = self.request.user)

class BlogDetailsView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()
    permission_classes = [IsAuthorOrReadOnly]

    def perform_update(self, serializer):
        serializer.save(author = self.request.user)


class CommnetlistView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all().order_by('-created')
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author = self.request.user)


class CommnetDetailsView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentDetailsSerializer
    queryset = Comment.objects.all()  
    permission_classes = [IsAuthorOrReadOnly]

    def perform_update(self, serializer):
        serializer.save(author = self.request.user)