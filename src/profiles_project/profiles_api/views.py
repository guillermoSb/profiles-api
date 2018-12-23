from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken 
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from . import permissions

from . import serializers
from . import models

# Create your views here.

# This is a class based view, which means that we can manually add the methods by ourselves.
class HelloApiView(APIView):
    """ Test API view """

    serializer_class = serializers.HelloSerializer

    def get(self, request, format=None):
        """ Returns a list of api views features """
        an_api_view = [
            'Uses Http methods as functions, GET, POST PATCH AND DELETE',
            'It is similar to a traditional django view',
            'Gives you the most controll of your logic',
            'Is mapped manually to urls'
        ]
        return Response({'message': 'Hello', 'an_api_view': an_api_view})

    def post(self, request):
        """ Create a hello Message with our name """
        serializer = serializers.HelloSerializer(data = request.data)
        if serializer.is_valid():
            name = serializer.data.get('name')
            message = 'Hello {0}'.format(name)
            return Response({'message': message})
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk=None):
        """ Handles Updating an object """
        return Response({"method": 'put'})

    def patch(self, request, pk=None):
        """ Handles Patching an object """
        return Response({"method": 'patch'})

    def delete(self, request, pk=None):
        """ Handles Deleting an object """
        return Response({"method": 'delete'})

class HelloViewSet(viewsets.ViewSet):
    """ Test Api View Set """
    serializer_class = serializers.HelloSerializer
    def list(self, request):
        """ Return a hello message """
        a_viewset = [
            'Uses actions',
            'LIST CREATE RETRIEVE UPDATE'
        ]
        return Response({'message': 'Hello', 'a_viewset': a_viewset})
    
    def create(self, request):
        """ Create a new hello message """
        serializer = serializers.HelloSerializer(data = request.data)
        if serializer.is_valid():
            name = serializer.data.get('name')
            message = 'Hello {0}'.format(name)
            return Response({'message': message})
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def retrieve(self, request, pk=None):
        """ Get an object by its id"""
        return Response({'http_method': 'GET'})
    def update(self, request, pk = None):
        """ Handles updating an object """
        return Response({"method": 'PUT'})
    def partial_update(self, request, pk = None):
        """ Handles patching an object """
        return Response({"method": 'PATCH'})
    def destroy(self, request, pk = None):
        """ Handles Deleting an object """
        return Response({"method": 'delete'})


class UserProfileViewSet(viewsets.ModelViewSet):
    """ Profiles crud """

    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)

class LoginViewSet(viewsets.ViewSet):
    """ Check email and pass and return an auth token """
    serializer_class = AuthTokenSerializer

    def create(self, request):
        """ Use the obtain Auth token to validate and create a token """

        return ObtainAuthToken().post(request)

class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """ CRUD profile feed """
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    permission_classes = (permissions.PostOwnStatus, IsAuthenticatedOrReadOnly)
    queryset = models.ProfileFeedItem.objects.all()
    
    def perform_create(self, serializer):
        """ Sets the user profile to the current user """
        serializer.save(user_profile = self.request.user)

class ContributorViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ContributorSerializer
    queryset = models.Contributor.objects.all()
    def get_queryset(self):
        return models.Contributor.objects.all()
    def perform_create(self, serializer):
        """ Sets the user profile to the current user """
        serializer.save(**serializer.validated_data)
    
    
