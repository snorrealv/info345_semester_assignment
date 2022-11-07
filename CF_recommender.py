import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
class CF_recommender:
    
    def __init__():
        pass

    # parameteret dataset has to have the columns; user_id, item_id, rating and Name
    def clean_data(dataset):
        return dataset
    
    def make_ratings_matrix(df):
        ratings_matrix = df.pivot_table(values='rating', index='user_id', columns='item_id')
        return ratings_matrix
    
    #takes a ratings matrix as parameter, normalises it based on user averages 
    # and swaps out nan values with 0
    def norm_ratings_matrix(ratings_matrix):
        norm_ratings_matrix = ratings_matrix.subtract(ratings_matrix.mean(axis=1), axis='rows')
        not_null = norm_ratings_matrix.fillna(0)
        return not_null
    
    def cosine_similarity_matrix(sim_matrix):
        cos = cosine_similarity(sim_matrix)
        cosim_matrix = pd.DataFrame(cos,index=sim_matrix.index)
        cosim_matrix.columns = sim_matrix.index
        return cosim_matrix
    
    def recommend(user_id):
        pass

    
    




