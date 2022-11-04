from django.db import models

from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Submission(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    userId = models.CharField(max_length=100)
    answers = models.JSONField()
    pageId = models.CharField(max_length=100)    

    # boolean for signal and interlan logic
    train_on_submission = models.BooleanField(default=False)
    final_submission = models.BooleanField(default=False)

    class Meta:
        ordering = ['created']
        
    def __str__(self):
        return f'{self.userId} on form {self.pageId}'

class Recommendations(models.Model):
    id = models.AutoField(primary_key=True)
    userId = models.CharField(max_length=200)
    recommendation_model = models.CharField(max_length=200, default="NaN")

    # def movies_default():
    #     return {"movies":["a","b","c"]}
    
    # #movies = models.JSONField('Recommendation', default=movies_default)
    # movies = models.ManyToManyField(Movies)

    user_description_short = models.CharField(default='', max_length=500)
    user_description_long = models.CharField(default='', max_length=1000)


    def __str__(self):
        return f'{self.userId} with model {self.recommendation_model}'
    

class UserRankings(models.Model):
    userId = models.CharField(max_length=200)
    movieId = models.IntegerField()
    rank = models.IntegerField()

    def __str__(self):
        return f'{self.userId} on movie {self.movieId}'

class FinalResult(models.Model):
    userId = models.CharField(max_length=200)
    answers = models.JSONField()
