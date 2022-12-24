from django.http import JsonResponse
import requests
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status


from .serializers import NoteSerializer,videoSerializer
from base.models import Note ,video


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        # ...

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/token',
        '/api/token/refresh',
    ]

    return Response(routes)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getNotes(request):
    user = request.user
    notes = user.note_set.all()
    serializer = NoteSerializer(notes, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def massageCreate(request):
    z = request.data
    response = requests.get(z['api']+'/api?input='+z['message'])
   
    if response.status_code == 500 :
        return JsonResponse({'foo':'bar'})
    #convert reponse data into json
    if response.status_code != 404:
      users = response.json()
      re=users['response']
      a=len(z['message'])
      re=re[a:]
      z['reply']=re
   
    z['user'] = request.user.id
   
    serializer = NoteSerializer(data=z)
    if serializer.is_valid():
	    serializer.save()
    return Response(serializer.data)


@api_view(['POST'])
def uploadvideo(request):
    item =videoSerializer(data=request.data)
  
    # validating for already existing data

  
    if item.is_valid():
        item.save()
        return Response(item.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)    


@api_view(['GET'])
def videolist(request):
    
    # checking for the parameters from the URL
    
    items = video.objects.all()
  
    # if there is something in items else raise error
    serializer = videoSerializer(items, many=True)
    return Response(serializer.data)     