from django.urls import path
from . import views



urlpatterns = [
    path('stream/<int:pk>/', views.get_streaming_video, name='stream'),
    path('', views.get_list_video, name='home'),
    path('login/', views.MyprojectLoginView.as_view(), name='login'),
    path('register/', views.RegisterUserView.as_view(), name='register'),
    path('logout/', views.MyprojectLogoutView.as_view(), name='logout'),
    path('video/<int:pk>/like/', views.AddLike.as_view(), name='like'),
    path('video/<int:pk>/dislike/', views.AddDislike.as_view(), name='dislike'),
]
