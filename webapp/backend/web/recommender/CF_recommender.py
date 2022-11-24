import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class CF_recommender:
    df = pd.read_csv("/data/all_recipes/user-item-rating.csv",  on_bad_lines='skip', sep = '\t', names = ['user_id', 'item_id', 'rating'])
    num_similar_users = 21

    def __init__():
        pass


    def make_ratings_matrix():
        df = CF_recommender.df
        ratings_matrix = df.pivot_table(values='rating', index='user_id', columns='item_id')
        return ratings_matrix
    
    def add_new_data(user_id, item_id, rating):
        df = CF_recommender.df
        new_row = {'user_id': user_id, 'item_id': item_id, 'rating': rating}
        CF_recommender.df = df.append(new_row, ignore_index = True)
    
    def save_df_to_file():
        CF_recommender.df.to_csv('./df_CF_recommender.csv')

    # takes a ratings matrix as parameter, normalises it based on user averages 
    def norm_ratings_matrix():
        ratings_matrix = CF_recommender.make_ratings_matrix()
        norm_ratings_matrix = ratings_matrix.subtract(ratings_matrix.mean(axis=1), axis='rows')
        return norm_ratings_matrix
    
    def cosine_similarity_matrix():
        norm_matrix = CF_recommender.norm_ratings_matrix()
        not_null = norm_matrix.copy().fillna(0)
        cos = cosine_similarity(not_null)
        cosim_matrix = pd.DataFrame(cos,index=not_null.index)
        cosim_matrix.columns = not_null.index
        return cosim_matrix
    
    # Group data by user, count number of ratings and shows the mean for each user: 
    def aggregate_by_user():
        df = CF_recommender.df
        aggregate_by_user = df.groupby('user_id').agg(mean_rating = ('rating', 'mean'), 
        number_of_ratings = ('rating', 'count')).reset_index()

        return aggregate_by_user


    def recommend(user_id, top_recipes = 10, new_data=None):
        if new_data:
            for data in new_data:
                CF_recommender.add_new_data(data)
        matrix = CF_recommender.cosine_similarity_matrix()
        norm_matrix = CF_recommender.norm_ratings_matrix()

        # The users that have the highest similarity with given user
        similar_users = matrix[user_id].sort_values(ascending = False)[:CF_recommender.num_similar_users]
        
        # Drops given user from similar users
        similar_users.drop(index = user_id, inplace = True)
        sim_user_recipes = norm_matrix[norm_matrix.index.isin(similar_users.index)].dropna(axis=1, how='all')

        # Finds all recipes that given user has rated, and removed these from sim_user_recipes because we dont want to recommend recipes 
        # that the user has already tried.
        userID_rated = norm_matrix[norm_matrix.index == user_id].dropna(axis=1, how= 'all')
        sim_user_recipes.drop(userID_rated.columns,axis=1, inplace= True, errors = 'ignore')
        
        # Dictionary to store all predicted item ratings
        item_ratings = {}

        # The given users average rating
        aggregate_by_user = CF_recommender.aggregate_by_user()
        user_avg = aggregate_by_user[aggregate_by_user['user_id']==user_id]['mean_rating'].item()

        # Predicting the rating for each of the recipes in sim_user_recipes
        for i in sim_user_recipes.columns:
            sim_scores = similar_users.copy()
            recipe_ratings = sim_user_recipes[i]
            idx = recipe_ratings[recipe_ratings.isnull()].index
            recipe_ratings = recipe_ratings.dropna()
            sim_scores = sim_scores.drop(idx)
            sim_score_sum = sim_scores.sum()
            if sim_score_sum == 0:
                sim_score_sum = 1
            wmean_rating = user_avg + (np.dot(sim_scores, recipe_ratings) / sim_score_sum)
            item_ratings[i] = wmean_rating
        
        # Turning the dict into a dataframe, sorting the dataframe by predicted ratings,
        #  and getting the top 10 recipes
        item_ratings = pd.DataFrame(item_ratings.items(),columns=['recipe', 'predicted_rating'])
        ranking_recipe_scores = item_ratings.sort_values(by='predicted_rating', ascending=False)
        recipes_to_recommend = ranking_recipe_scores.head(top_recipes)

        return recipes_to_recommend

    

