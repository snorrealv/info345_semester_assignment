from urllib.request import Request
from rest_framework import serializers
from handler.models import Submission, Recommendations, UserRankings


# Creating serializer class

class SubmissionSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only = True)
    userId = serializers.CharField(max_length=100)
    pageId = serializers.CharField(max_length=100)
    train_on_submission = serializers.BooleanField()
    final_submission = serializers.BooleanField()
    answers = serializers.JSONField()

    def create(self, validated_data):
        return Submission.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.userId = validated_data.get('user_id', instance.user_id)
        instance.answers = validated_data.get('answers', instance.answers)
        return instance


class ImageSerializerField(serializers.Field):
    def to_representation(self, values):
        return values['']
    def to_internal_value(self, data):
        return


class RecommendationSerializer(serializers.Serializer):
    userId = serializers.CharField()
    recommendation_model = serializers.CharField()
    movies = MovieSerializer(many=True)

class UserRankingsSerializer(serializers.Serializer):
    userId = serializers.CharField()
    movieId = serializers.IntegerField()
    rank = serializers.IntegerField()

    def create(self, validated_data):
        return UserRankings.objects.create(**validated_data)

# For any other classes that needs serializing, the same can be achieved with ModelSerilaizer class, 
# see https://www.django-rest-framework.org/tutorial/1-serialization/#using-modelserializers
# I have simply chosen to use the manual method due to our JSONField(). 
