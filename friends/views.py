# from django.shortcuts import render
# from django.http import HttpResponse
from friends.models import User,Friends,Posts, Ids, FriendRequests, Likes
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from friends.serializers import Userserializer,Friendserializer,Postsserializer,IdsSerializer ,FriendRequestserializer, Likesserializer
from rest_framework.exceptions import AuthenticationFailed
import jwt
import datetime
from django.db.models import Q
import requests
from rest_framework import status
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import filters
from rest_framework import generics

class UserViewSet(viewsets.ModelViewSet):
     
    search_fields = ['user_name','myId','city']
    filter_backends = (filters.SearchFilter,)
    queryset=User.objects.all()
    serializer_class=Userserializer 
    #serializer=Userserializer(queryset,many=True)

    
class UserUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = Userserializer

class FriendsViewSet(viewsets.ModelViewSet):
     
    search_fields = ['self_id']
    filter_backends = (filters.SearchFilter,)
    queryset=Friends.objects.all()
    serializer_class=Friendserializer 

class LikesViewSet(viewsets.ModelViewSet):
     
    search_fields = ['post_id']
    filter_backends = (filters.SearchFilter,)
    queryset=Likes.objects.all()
    serializer_class=Likesserializer

class FriendRequestViewSet(APIView):

    def get(self, request, pk=None):
        if pk is None:
            instances = FriendRequests.objects.all()
            serializer = FriendRequestserializer(instances, many=True)
            return Response(serializer.data)
        try:
            instance = FriendRequests.objects.get(pk=pk)
            serializer = FriendRequestserializer(instance)
            return Response(serializer.data)
        except FriendRequests.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    def post(self, request):
        serializer = FriendRequestserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk=None):
        if pk is None:
            FriendRequests.objects.all().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        try:
            instance = FriendRequests.objects.get(pk=pk)
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except FriendRequests.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class SearchView(APIView):
    
    def get(self, request, request_to=None):
        if request_to is None:
            instances = FriendRequests.objects.all()
        else:
            instances = FriendRequests.objects.filter(request_to=request_to)
        
        serializer = FriendRequestserializer(instances, many=True)
        return Response(serializer.data)

class PostsViewSet(viewsets.ModelViewSet):
     
    search_fields = ['=self_id']
    filter_backends = (filters.SearchFilter,)
    queryset=Posts.objects.all()
    serializer_class=Postsserializer 
    # return Response(Postsserializer.data)

def get_user_by_id(request, myId):
    try:
        man = User.objects.get(pk=myId)
        data = {
            "user_name": man.user_name,
            "about": man.about,
            
            # Add other fields as needed
        }
        return JsonResponse(data)
    except User.DoesNotExist:
        return JsonResponse({"error": "man not found"}, status=404)



class RegisterView(APIView):
    def post(self, request):
        serializer=IdsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class LoginView(APIView):
    def post(self, request):
        email=request.data['email']
        password=request.data['password']
        user=Ids.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed('user not found')
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect Password')
        payload={
            'id':user.id,
            'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=60),
            'iat':datetime.datetime.utcnow()
        }
        token=jwt.encode(payload,'secret',algorithm='HS256')
        response=Response()
        response.set_cookie(key='jwt',value=token,httponly=True)
        response.data={
            'jwt':token
        }
        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        try:
            payload=jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')
        user=Ids.objects.filter(id=payload['id']).first()
        serializer=IdsSerializer(user)
        return Response(serializer.data)

class UserView(APIView):
    def get(self, request):
        token=request.COOKIES.get('jwt')
        print("token = ")
        print(token)
        response=Response()
        response.data={
            'jwt':token
        }
        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        try:
            payload=jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')
        user=Ids.objects.filter(id=payload['id']).first()
        serializer=IdsSerializer(user)
        return Response(serializer.data)

class LogoutView(APIView):
    def post(self, request):
        response=Response()
        response.delete_cookie('jwt')
        response.data={
            'message': 'logged out'
        }
        return response

