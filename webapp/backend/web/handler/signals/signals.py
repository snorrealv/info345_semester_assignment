from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist

from ..models import UserRankings, Recommendations, Submission, FinalResult, Recipe, RecipeRanked
from ..tasks import run_recommendations

import json

# Submission signals
@receiver(post_save, sender=Submission)
def sub_post_save(sender, instance, created, *args, **kwargs):
    # On submission creation, we initualize a recommendation, and train a model for the
    # user, afterwards we update this recommendation with the recommendation itself.

    if created:
        if instance.train_on_submission:
            # Get userrankings
            q = UserRankings.objects.filter(userId = instance.userId)
            ratings = [[int(i.userId),int(i.movieId), int(i.rank)] for i in q]
            print('ratings', ratings)

            # we remove all ratings after sending them to the models, the
            # user results are also stored in the submissions, these are
            # only used for training.
            for movie in q:
                movie.delete()

            data = {"userId": instance.userId, "recipes": ratings}
            # {"userID": userID, "movies": [movieID, movieID, movieID...]}
            # Initualize the recommendation object

            # Save the original choices in recommendation with None
            # orig_recommendation = Recommendations(userId = instance.userId)
            # orig_recommendation.save()
            # orig_recommendation.recommendation_model = 'original'

            # for objec in data.items():
            #     for obj in objec[1]:
            #         try:
            #             orig_recommendation.movies.add(Movies.objects.get(movieId = obj))
            #         except ObjectDoesNotExist:
            #             print(f'Movie with movieId: {obj} not found.')
            
            # orig_recommendation.save()

            # Start recommender task with user ID and data
            run_recommendations.delay(userId = instance.userId, data=data, model='VCS')
            run_recommendations.delay(userId = instance.userId, data=data, model='CF')
        
        if instance.final_submission:
            print('FINAL SUBMISSION')
            # Creates final submission object and adds to database.
            # (this also fires the signal result_post_save())
            user_submissions = Submission.objects.filter(userId = instance.userId)
            print(user_submissions)
            # dict variable to be stored to json field in FinalResult()
            user_final_submission = {
                                    "userId":instance.userId,
                                    "formAnswers": {},
                                    "recommendations": {},
                                    }

            # iterate and add all form answers
            for submission in user_submissions:
                user_final_submission['formAnswers'][submission.pageId] = submission.answers
            
            # get movies recommended to users and add to recommendation field
            # there can be several down the line so we're accounting for that
            user_recommendations = Recommendations.objects.filter(userId = instance.userId)
            for recommendation in user_recommendations:
                user_final_submission['recommendations'][recommendation.recommendation_model] = [f'{recipe.recipe_id}' for recipe in recommendation.recipes.all()]

            # store results in db
            stored_user_submission = FinalResult(userId = instance.userId, answers=user_final_submission)
            stored_user_submission.save()

# Recieved that logs final results into json file:
@receiver(post_save, sender=FinalResult)
def result_post_save(sender, instance, created, *args, **kwargs):
    # When a final result have been given, it should be stored into a json file on the server
    # at a later date this can be a object storage at e.g. IBM.
    print('FINAL SUBMISSION')
    if created:
        location = '/data/user_responses/'
        #location = '../../../../userstudy_results/als_US/'
        json_content = []

        contents = FinalResult.objects.all()
        for content in contents:
            json_content.append(content.answers)

        json_object = json.dumps(json_content, indent=2)
        with open(location + 'user_responses.json', 'w') as file:
            file.write(json_object)
            