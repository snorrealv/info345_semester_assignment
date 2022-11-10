from handler.models import ( 
    Submission, Recommendations, UserRankings, Recipe, Image
)
from handler.custom_renderers import JPEGRenderer
from handler.serializers import (
    SubmissionSerializer, RecipeSerializer,
    RecommendationSerializer, UserRankingsSerializer
    )

from rest_framework import generics, pagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import filters
from rest_framework import status
from rest_framework.decorators import api_view

from django_filters.rest_framework import DjangoFilterBackend


from django.http import HttpResponse, JsonResponse
from django.http import Http404
from urllib.request import urlopen
import random
import json
import requests as rq

# Pagination class
class RecipePagination(pagination.PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 20


class Submissions_list(generics.ListCreateAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

class Submissions_detail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

class Recipe_list(generics.ListAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    # set pagination
    pagination_class = RecipePagination

    # for serach
    filter_backends = [filters.SearchFilter]
    search_fields = ['^title']

class Recommendation(APIView):
    def get_object(self, pk, tk):
        # in some edge cases we have several recommendations from users
        # to combat this we simply return one object.
        if tk:
            try:
                return Recommendations.objects.filter(userId=pk, recommendation_model=str(tk))[:1].get()
            except:
                raise Http404
        else:
            try:
                return Recommendations.objects.filter(userId=pk)[:1].get()
            except:
                raise Http404
        

    def get(self, request, pk, format=None, *args, **kwargs):
        # pk = userId
        # tk = recommenderId
        tk = self.kwargs.get('pk_model', None)
        recommendation = self.get_object(pk, tk)

        
        while recommendation.recommendation_model == 'NaN':
            recommendation = self.get_object(pk)
        serializer = RecommendationSerializer(recommendation)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ReccomendationSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class ImageApiView(generics.RetrieveAPIView):

    renderer_classes = [JPEGRenderer]

    def get(self, request, *args, **kwargs): 
        try:
            queryset = Image.objects.get(slug=self.kwargs['id']).image
    
            data = queryset
            return Response(data, content_type='image/jpg')
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

class StartingRecipes(APIView):
    def get_object(self):
        starting_recipes = ['1880','1924', '2006', '2055', '1854']
        try:
            return Recipe.objects.filter(recipe_id__in=starting_recipes)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, format=None, *args, **kwargs):
        recipe = self.get_object()
        

        serializer = RecipeSerializer(recipe, many=True)
        return Response(serializer.data)

class Rating(APIView):
    def get_object(self, pk, tk):
        try:
            return UserRankings.objects.get(userId=pk)
        except UserRankings.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        UserRankings = self.get_object(pk)
        serializer = UserRankingsSerializer(UserRankings)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        UserRankings = self.get_object(pk)
        serializer = UserRankingsSerializer(UserRankings, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        serializer = UserRankingsSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        UserRankings = self.get_object(pk)
        UserRankings.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

