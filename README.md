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
│   └── VCS_recommender.py
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
Quickly about each content:
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

**exploring_answers.ipyng** explores our user data, this is also where we found our user survey statistics, so this file is of value for anyone looking into this. Important functions here are our `reweight` funciton which stands for the 
$$rsw_{score}= item_{rated} \times (sw_{score} \times aw)$$
function logic, we also calculate the absolute preference score here:
$$absPreference_{s} = \frac{\sum_{r\in Q_s} r_{q1}  \times r_{q2} \times r_{q3}}{|Q|}$$

and our relative preference score:
$$relPreference_{s} = \frac{\sum_{r\in Q_s} r_{q1}  \times r_{q2} \times r_{q3}}{|Q_s|}$$