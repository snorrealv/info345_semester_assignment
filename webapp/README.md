## Recsys Project v0.1 
Recsys Project is aiming to create a Framework to allow for easy user-testing of recommender systems in an intuitive way. 

People involved: **Snorre Alvsvåg**

##### 1.0 Time estimations
With my current employment and how the month of June is looking, having a first draft of the framework done by the end of June before summer vacation seems plausible. There is a chance it might get postponed if other work arises, as this project is a long term lower priority project. I will however plan to have a first draft ready by June 30th.

Further update will be publised when needed. 
#### 2.0 Roadmap
<img width="1919" alt="Screenshot 2022-06-10 at 11 20 03" src="https://user-images.githubusercontent.com/55574575/173034417-8f26427c-c8f2-4d22-b8d7-8583e87195f2.png">

#### 3.0 Known Future Obstacles
None as of date.
#### 4.0 Decisions
##### 4.1 Technologies
Alongside input from Anastasiia I have decided to use a stack based around a Docker + Django backend, and a Astro frontend. Astro allows for seamless integration of several frontend javascript libraries if the end-user wishes, and most notably, easy markdown rendering with the inclusion of components, making the process of creating surveys a really simple process. See 5.0 for more information about the technology stack.

#### 5.0 Technology Stack
*(to be written)*

#### 6.0 Program Pipeline
<img width="1919" alt="Screenshot 2022-06-10 at 11 19 31" src="https://user-images.githubusercontent.com/55574575/173034243-503915b7-7413-4cb4-b5e1-864c9889dbb6.png">

##### 6.1 Questionnaires
Astro Frontend, javascript like language that compiles to native, lets users implement any popular javascript library components that they create. Allows for simple markdown rendering. Fully delivered by framework, but allows for great customization by users. 

##### 6.2 Backend
Django Backend, Django due to Python being such a versatile language, and the Django Admin platform will allow for easy management of the systems. Partially delivered by framework. The Django Web framework will be delivered so that its already setup towards the questionnaires and the frontend, and the database will contain tables to deal with these. The recommender system itself will come with a template, but should be changed on a per study basis, as well as implementing database tables for relevant data. 

We could in the future try and implement semi-automatic database creation from cleaned datasets using [csvkit](https://csvkit.readthedocs.io/en/1.0.7/), this is not a priority as of now however.

##### 6.3 Frontend
Astro Frontend, same system as the questionnaires, will come with predefined layouts for data, such as a netflix like UI, newspaper like UI and the like, but also allow for custom components and layouts built by the user in their prefered frontend language.``
