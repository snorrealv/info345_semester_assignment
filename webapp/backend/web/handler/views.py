from handler.models import ( 
    Submission, Recommendations, UserRankings
)
from rest_framework import status
from rest_framework.decorators import api_view
from handler.serializers import (
    SubmissionSerializer,
    RecommendationSerializer, UserRankingsSerializer
    )

from rest_framework import generics, pagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import filters

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

class Movie_list(generics.ListAPIView):
    queryset = Movies.objects.all()
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