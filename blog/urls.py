from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.Post_list, name='Post_list'),
    path('post/<int:id>/', views.post_details, name='post_details'),
    path('post/<int:id>/like/', views.Post_like, name='post_like'),
    path('post/create/', views.post_create, name='post_create'),
    path('post/update/<int:id>/', views.post_update, name='post_update'),
    path('post/delete/<int:id>/', views.Post_delete, name='Post_delete'),
    path('signup/', views.signup_view, name='signup'),
    path('profile/', views.profile_view, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
