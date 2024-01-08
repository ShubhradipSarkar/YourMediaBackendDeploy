from django.contrib import admin
from django.urls import path, include
from friends.views import UserViewSet,FriendsViewSet,PostsViewSet ,FriendRequestViewSet, LikesViewSet
from .views import RegisterView, LoginView, UserView, LogoutView, SearchView, UserUpdateView
from rest_framework import routers
from . import views

router=routers.DefaultRouter()
router.register(r'Userss',UserViewSet)
router.register(r'Friends',FriendsViewSet)
router.register(r'Posts',PostsViewSet)
router.register(r'Likes', LikesViewSet)

#router.register(r'FriendRequests',FriendRequestViewSet)

urlpatterns = [
    path('',include(router.urls)),
    path('Userss/<int:user_id>/', views.get_user_by_id, name='get_user_by_id'),
    path('register',RegisterView.as_view()),
    path('login',LoginView.as_view()),
    path('user',UserView.as_view()),
    path('logout',LogoutView.as_view()),
    path('friendRequest/', FriendRequestViewSet.as_view(), name='FriendRequestViewSet'),
    path('friendRequest/<int:pk>/', FriendRequestViewSet.as_view(), name='friendAccepted'),
    path('SearchView/<int:request_to>/', SearchView.as_view(), name='SearchView'),
    path('UserUpdate/<int:pk>/', UserUpdateView.as_view(), name='user-update'),
    
    #path('search/', search_users.as_view(), name='search_users'),
    #path('Posts/<int:user_id>/', views.get_post_by_id, name='get_post_by_id'),
]
 