from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    ApiRoots,
    UserRegisterApiView,
    UserDetailsApiView,
    UserProfilelistView,
    UserProfileDetailsView,
    BlogListView,
    BlogDetailsView,
    CategroyListView,
    CategroyDetailsView,
    CommnetlistView,
    CommnetDetailsView
)



urlpatterns = [
    path('', ApiRoots.as_view()),
    path('user/', UserRegisterApiView.as_view(), name = 'user-list'),
    path('profile/', UserProfilelistView.as_view(), name = 'profile-list'),
    path('category/', CategroyListView.as_view(), name = 'categroy-list'),
    path('blog/', BlogListView.as_view(), name = 'blog-list'),
    path('comments/', CommnetlistView.as_view(), name = 'comment-list'),
    path('user/<int:pk>', UserDetailsApiView.as_view(), name = 'user-detail'),
    path('profile/<int:pk>', UserProfileDetailsView.as_view(), name = 'profile-detail'),
    path('category/<int:pk>', CategroyDetailsView.as_view(), name = 'categroy-detail'),
    path('blog/<int:pk>', BlogDetailsView.as_view(), name = 'blog-detail'),
    path('comments/<int:pk>', CommnetDetailsView.as_view(), name = 'comment-detail'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/', include('rest_framework.urls'))


]
