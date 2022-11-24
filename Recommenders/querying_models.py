import pandas as pd

from CF_recommender import CF_recommender
from VCS_recommender import VCS_recommender

user_id=80477
submission = {"1854": "5", "1880": "4", "1924": "5", "2002": "2", "2055": "1","7011": "5", "6002": "4", "5967": "5", "5003": "4", "50": "1"}

# VCS recommendation:
VCS = VCS_recommender()
VCS_results = VCS.recommend(user_id)
print(VCS_results[['recipe','simularity_adjustment','new_index']])

# CF recommender
CF = CF_recommender
for i in submission.keys():
    # add new data
    CF.add_new_data(user_id,i,submission[i])

CF_results = CF.recommend(user_id=user_id, top_recipes=30)

print(CF_results)