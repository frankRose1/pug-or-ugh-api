# Pug Or Ugh API
Paw left or right to help potential dog owners find the dog of their dreams! This is a backend restful API built with the Django REST framework that allows users to sign up, set their preferences, and search for and like dogs. 

## App Features
- Tests coverage is at 95%
- Serializers are used to validate incoming data
- Models properly handle relationship between users, dogs, and user preferences
- Token auth controls access to the API
- ```pug_or_ugh/scripts/data_import.py``` is a script that will populate the database with initial data if needed.

## Endpoints
*To get the next liked, disliked, or undecided dog. (pk will determine the current dog). 404s are returned when the list of dogs has been exhausted*
- ```/api/dog/<pk>/liked/next/  GET``` will get the users next liked dog
- ```/api/dog/<pk>/disliked/next/  GET``` will get the users next disliked dog
- ```/api/dog/<pk>/undecided/next/  GET``` will get the users next undecided dog. user preferences are used to query that database for dogs that
    match.

*To update a dog's status to liked, disliked, or undecided. These views will also create a UserDog relationship if it doesn't already exist*
- ```/api/dog/<pk>/liked/  PUT``` will update the user/dog relationship to "liked"
- ```/api/dog/<pk>/disliked/  PUT``` will update the user/dog relationship to "disliked"
- ```/api/dog/<pk>/undecided/  PUT``` will update the user/dog relationship to "undecided"


*To create, update, or get a user's preferences*
- ```/api/user/preferences/  GET``` will return the preferences, or a 404 if they havn't been created
- ```/api/user/preferences/  POST``` will create the preferences, or return a 400 if they've already been created
- ```/api/user/preferences/  PUT``` will update the preferences, or return a 404 if they havn't been created

*Registration/Authentication*
- ```/api/user/  POST``` email, username, and password are required
- ```/api/user/login  POST``` will return an access token if provided credentials(username and password) are correct
- To authenticate requests to the API set the Authorizaion headers like this:
    ``` 'Authorization': 'Token {your_token_here}'

## Errors
- 400 errors are returned for invalid data sent to the API, or trying to search dogs without having set up preferences
- 401 errors are returned for unauthenticated requests
- 404 errors are returned for routes and resources that don't exist.


## Tests
- django-nose is used as the test runner
- coverage will print out a report detailing the tests
- to run tests run ```pipenv run python manage.py test``` in the terminal

## Technologies Used
- django
- django-rest-framework
- django-nose
- coverage
