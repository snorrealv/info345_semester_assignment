import sklearn
import pandas as pd
import numpy as np
from CF_recommender import CF_recommender

class VCS_recommender:
    def __init__(self):
        self.base_recommendation_model = CF_recommender
        self.df = pd.read_csv('../data/features.csv')
        self.original_recommendation = None


    def __get_orignial_recommendation(self, user_id):
        recommendation = self.base_recommendation_model.recommend(user_id=user_id, top_recipes=30)
        self.original_recommendation = recommendation.reset_index(drop=True)


    @staticmethod
    def __cosine_similarity(a,b):
        return np.dot(a,b) / ( (np.dot(a,a) **.5) * (np.dot(b,b) ** .5) )


    @staticmethod
    def __new_rank(margin, sim, star):
        star_rating = {'1':-2, '2':-1, '3':0, '4':1, '5':2}
        simweight = margin - ((1-sim)*100)
        # print(f'{star}, {star_rating[star]}, {margin},ss {(1-sim)*100}, {sim}, {simweight}')
        return star_rating[star] * (simweight * 0.5)


    def __findsimular(self, id:int, values = None, submission = None):
        # get features for item:
        a = self.df[self.df.id==id].values
        try:
            if not values: values = self.df.values
        
        except Exception as e:
            pass

        if a.any():
            l = []
            for key, value in enumerate(values):
                l.append([id, int(value[-1]), self.__cosine_similarity(a[0][:-1],value[:-1]), submission[str(int(value[-1]))]])
            DF = pd.DataFrame(l, columns =['parent_id','sim_id', 'simularity','rated'])

            DF = DF[DF.simularity >= 0.8]
            
            final = []
            for simulated in DF.itertuples():
                final.append(self.__new_rank(margin=20, sim=simulated.simularity, star=simulated.rated))

            
            return (sum(final)/len(final))


    def __getvalues(self, submission):
        id_list = submission.keys()
        id_list = [int(i) for i in id_list]
        values = self.df[self.df['id'].isin(id_list)].values
        return values


    def recommend(self, user_id, submission = None,):
        
        if not submission:
            submission = {"1854": "5", "1880": "4", "1924": "5", "2006": "4", "2055": "1","7011": "5", "6002": "4", "5967": "5", "5003": "4", "9319": "1"}

        final = []

        values = self.__getvalues(submission)
        new_values = []
        self.__get_orignial_recommendation(user_id)
        for rec in self.original_recommendation.itertuples():
            new_values.append([rec.recipe, rec.predicted_rating, rec.Index, self.__findsimular(rec.recipe, values=values, submission=submission),])

        for key, value in enumerate(new_values):
            if value[-1]:
                new_values[key].append((value[2]+1)-value[-1])
            # print(findsimular(rec.recipe, values=values, submission=submission))
        final_df = pd.DataFrame(new_values, columns=['recipe_id', 'predicted_rating','index','simularity_adjustment','new_index'])
        final_df = final_df.sort_values(by='new_index')

        return final_df

rec = VCS_recommender()
l = rec.recommend(455)
print(l)