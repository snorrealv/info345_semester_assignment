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
Here just follow the prompts.

After this the entire site can be used and reached on IP
**0.0.0.0**

**Possible pitfalls:**
You might have to delete all contents except for the `__init__.py` file in `/backend/web/handler/migratoins/` if you get a error whilst starting the program in STEP 1. 

### Running Frontend for Development
Theres already a built and compiled version of the frontend served through the docker-compose file, so in theory you should not need to touch Node or the frontend. However if you want to make changes or poke around:

Ensure you have node installed, I've operated with node 18, but node 16 should also sufice.

from `/frontend` folder, run `npm install`
run: `npm install astro`
run: `npm run dev`

To preview chagnes you can look at **localhost:3000**, or to commit and see changes on 0.0.0.0:

run: `npm run build`.

This will rebuilkd the frontend with whatever changes.

Enjoy!