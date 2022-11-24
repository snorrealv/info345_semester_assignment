## Recommender Framework Applied for Food!


## Setup guide:

### Backend Cold start:
Step 1:
From the root of the folder, run `docker-compose up --build`

Step 2: 
Open a new terminal and enter into the web container with the following command:
`docker exec -it DJANGO /bin/bash`

Step 3:
Load data into database with the following command:

`python manage.py load-item-profiles`

After this load the items into the database:
`python manage.py add-images-to-db`

Step 4:
Create your super user:
`python manage.py createsuperuser`
Here just follow the prompts

Done!

**Possible pitfalls:**
You might have to delete all contents except for the `__init__.py` file in `/backend/web/handler/migratoins/` if you get a error whilst starting the program in STEP 1. 

### Running Frontend for Development
Ensure you have node installed, I've operated with node 18, but node 16 should also sufice.

from `/frontend` folder, run `npm install`
run: `npm install astro`
run: `npm run dev`

After this everthing should be live!

have fun!