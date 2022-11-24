# Semester Assignment INFO345

This is the github repository following a semester assignment in INFO345, Recommender Systems, University of Bergen.

Thesis can be found here:

## Contents of this repository:
```
.
├── feature_extraction.py
├── features.py
├── image_crawler.py
├── conda_requirements.txt
├── requirements.txt
├── Notebooks
│   ├── basic_recommender.ipynb
│   ├── exploring_answers.ipynb
│   ├── feature_extraction.ipynb
│   └── features_recommender.ipynb
├── Recommenders
│   ├── CF_recommender.py
│   ├── VCS_recommender.py
│   └── querying_models.py
├── data
│   ├── all_recipes
│   ├── features.csv
│   ├── giallozaferano_dataset.xlsx
│   ├── images
│   ├── item-profiles2.csv
│   ├── user-item-rating.csv
│   ├── user_responses
│   └── user_responses.json
└── webapp
    ├── README.md
    ├── backend
    ├── docker-compose.yml
    ├── documentation
    └── frontend
```
Quickly about each folder:
### Root folder
In the root folder you can find three scripts aswell as some requirements files containing the pip packages needed to run the scripts and algorythms in this repository. These are:
 - requirements.txt
 - conda_requirements.txt

Use these if needed, they are identical but the conda_requirements.txt is usefull if youre running miniconda on e.g. an M1 mac.
#### Scripts
**features.py** contains a range of functions for extracting low level visual features from images, inspired by code found in: https://github.com/dakvaol/vis.features/blob/main/thesis_project/features.py.

**feature_extracion.py** calls the features.py script as a module to extract the features from our images in `/data/images`.

**image_crawler.py** is a bs4 based crawler grabbing images for the items `from data/item-profiles2.csv`.

### Notebooks
The notebook folder contains notebooks used througout this course, these are messy and might not run at first glance, as they have been used and misused for some time. However shortly:

**basic_recommender.ipynb** explores the creation process and some analysis of our collaborative filtering model, it includes some scoring methods aswell. 

**feature_recommender.ipynb** explores the creation process of our hybrid recommender model.

**feature_extraction.ipynb** explores the creation processs of `feature_extraction.py`.

**exploring_answers.ipyng** explores our user data, this is also where we found our user survey statistics, so this file is of value for anyone looking into this. Important functions here are our `reweight()` funciton which stands for the 
$$rsw_{score}= item_{rated} \times (sw_{score} \times aw)$$
function logic, we also calculate the absolute preference score here:
$$absPreference_{s} = \frac{\sum_{r\in Q_s} r_{q1}  \times r_{q2} \times r_{q3}}{|Q|}$$

and our relative preference score:
$$relPreference_{s} = \frac{\sum_{r\in Q_s} r_{q1}  \times r_{q2} \times r_{q3}}{|Q_s|}$$

as well as most other math considering user preference analysis.

### Recommenders 
This is the folder housing both our recommenders, these are built as objects so that they can be called, and hold important functions. Theres also a `querying_models.py` file here which shows you how you can query the models.

**CF_recommender.py** contains all the logic needed to make a collaborative recommendation, and allows through the `CF_recommender` method to train and query the model. 

**VCS_recommender.py** contains all the logic needed to make a VCS recommendation, and allows through the `VCS_recommender()` method to train and query the model.

**querying_models.py** is a script where you can play around with the models and see how we interface with them, they are set up now with the test data and user id we showed off in the paper.

**PS:** you can see how the models are implemented in our webapp by going to: '/webapp/backend/web/handler/tasks.py', or look below:
```python
# ==================== CF ==========================
    if model == 'CF':
    recommendation_object = Recommendations(userId=userId, recommendation_model = model)
        recommendation_object.save()
         
        Recommender = CF_recommender.CF_recommender
        for i in data["recipes"]:
            Recommender.add_new_data(i[0],i[1],i[2])
        recommendation_data = Recommender.recommend(user_id=int(userId), top_recipes=30)
        
        print('CF', recommendation_data)

    # ==================== VCS ==========================
    if model == 'VCS':
        recommendation_object = Recommendations(userId = userId, recommendation_model = model)
        recommendation_object.save()

        Recommender = VCS_recommender.VCS_recommender()
        recommendation_data = Recommender.recommend(new_data=data, user_id=int(userId))

    # ==================== --- ==========================
        print('VCS', recommendation_data)
    for objec in recommendation_data.itertuples():
        recipe = RecipeRanked(recipe = Recipe.objects.get(recipe_id = objec.recipe), rank=1)
        recipe.save()
        recommendation_object.recipes.add(recipe)
        recommendation_object.save()
```
This way you wont have to dig too much into the webapp.


### Data
The data folder is expected to contain the following data:
```
.
├── features.csv
├── images
├── user_responses.json
└── all_recipes/
    ├── BMJ-data-all--b-new.csv
    ├── item-profiles1.csv
    ├── item-profiles2.csv
    ├── item-profiles3.csv
    ├── readme.md
    └── readme.txt
```
All of this is present except for the all_recipes dataset, this is removed because it was copyrighted, and this repository is public. You can simply download from the right source and replace to match the layout shown above.

### webapp
This folder containes the webapp that we used to run our userstudy, it has its own guide you can follow to launch the user study locally on your computer, using node and docker, please refer to the README.md file present in `/webapp/README.MD`