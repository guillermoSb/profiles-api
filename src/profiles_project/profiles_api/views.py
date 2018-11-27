from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.

class HelloApiView(APIView):
    """ Test API view """

    def get(self, request, format=None):
        """ Returns a list of api views features """
        an_api_view = [
            'Uses Http methods as functions, GET, POST PATCH AND DELETE',
            'It is similar to a traditional django view',
            'Gives you the most controll of your logic',
            'Is mapped manually to urls'
        ]
        return Response({'message': 'Hello', 'an_api_view': an_api_view})