from celery import shared_task
from django.db.models.signals import post_save
from django.dispatch import receiver

from recommender import CF_recommender, VCS_recommender
from .models import Recommendations, Recipe, RecipeRanked

@shared_task(bind=True)
def run_recommendations(self, userId, data, model = None):

    # Incoming Data:
    # {"userID": userID, "movies": [movieID, movieID, movieID...]}
    print(data)

    # Delete any previous recommendation made with ALS that is not a rerank
    # rerank to be added later
    try:
        prev_rec = Recommendations.objects.get(userId = userId, recommendation_model=model)
        prev_rec.delete()
    except:
        pass

    # ==================== CF ==========================
    if model == 'CF':
        recommendation_object = Recommendations(userId = userId, recommendation_model = model)
        recommendation_object.save()
         
        Recommender = CF_recommender.CF_recommender
        for i in data["recipes"]:
            Recommender.add_new_data(i[0],i[1],i[2])
        recommendation_data = Recommender.recommend(user_id=int(userId), top_recipes=30)
        
        print('CF', recommendation_data)
    #Recommender = als_recommender.ALSRecommender()
    #userId = int(userId)
    #Recommender.run_recommender(user_data=data, user_id=userId)
    #data = Recommender.recs
    #model = 'ALS'

    # ==================== VCS ==========================
    if model == 'VCS':
        recommendation_object = Recommendations(userId = userId, recommendation_model = model)
        recommendation_object.save()

        Recommender = VCS_recommender.VCS_recommender()
        recommendation_data = Recommender.recommend(new_data=data, user_id=int(userId))

    # ==================== --- ==========================
        print('VCS', recommendation_data)

    # recommendation.recipes.add(Recipe.objects.get(recipe_id = objec))

    # Find new, if there are two for some reason, pick one of them.
    # this filter()[:1].get() step is to avoid edge cases where the user went back and called 
    # the model twice. This also happends in the view and it always picks [:1]
    # recommendation = Recommendations.objects.filter(userId = userId, recommendation_model='NaN')[:1].get()

    for objec in recommendation_data.itertuples():
        recipe = RecipeRanked(recipe = Recipe.objects.get(recipe_id = objec.recipe), rank=1)
        recipe.save()
        recommendation_object.recipes.add(recipe)
        recommendation_object.save()
    
    # recommendation.recommendation_model = model
    # recommendation.save()