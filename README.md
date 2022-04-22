# The Microwave Broke Recipe Generator

## Overview:
Heroku URL: https://vast-peak-91474.herokuapp.com

The main-Objective of this web-app is to generate a repose based off of the ingredients present in the kitchen having salt, pepper, sugar, and the likes as default ingredients. 

## Installation Requirements:
Before running this app locally, you must pip or pip3 install the following dependencies:

* Flask
* requests
* python-dotenv
* flask-login
* Flask-SQLAlchemy
* psycopg2-binary
* termcolor
* sudo apt install postgresql
* npm i react-scripts

These are all of the required dependencies for this app. 

## Required API Keys, Database Key and Set Up:
Before running this app locally, you will also need to apply for 3 API keys and a Database:

* Spoonacular API
* Google Client ID
* Google Client Secret
* Required Database:
* Heroku Postgres Database

To apply for a Spoonacular API visit https://spoonacular.com/food-api and create an account. Keep track of API as you will need it later. 

To apply for Google Client visit https://console.cloud.google.com and sign in. 
Once signed in you will need to create a new project. Once you create a project you will be redirected to a new page. On that page click on “APIs & Services” then “Credentials”. Next, click “Create Credentials” and for type click “OAuth Client ID”. You will be redirected to a Create OAuth client ID page. For “Application Type” choose “Web application”. You are going to add an “Authorized JavaScript origins” and “Authorized redirect URIs”. To run locally, you will need to add your localhost to both of these fields. In the “Authorized redirect URIs” field make sure to add “/authorized” at the end of your localhost link. This redirects you to Google’s Authorized page. When finished you will create your OAuth Client ID. Next you will need to configure Consent Screen. For “User Type” you will choose “External.” Next you will fill out all of the required information on the following screens. Once you finish filling out all of the required information. Next you will click Create credentials again and follow the steps from above. This will then give you two keys you need. 


To create a Heroku Database please create an account with Heroku and begin these steps in your terminal:
* `heroku login -I ` This logs you into your heroku account
* `heroku create` Create a new Heroku app
* `heroku addons:create heroku-postgresql:hobby-dev` Create a new remote DB on your Heroku app
* `heroku config` This gives you the database url. Export this into the .env file.
* IF THE URL STARTS WITH postgres:, replace that with postgresql:

  
You will need to create a `.env` file in the same folder where the project is being held. In that .env file you need to export a few things listed below:
* `export DATABASE_URL` = ‘Heroku Database URL goes here’
* `export SECRET_KEY` = ‘Any key you want goes here’
* `export GOOGLE_CLIENT_ID` = ‘Google Client ID goes here’
* `export GOOGLE_CLIENT_SECRET` = ‘Google Client Secret goes here’
* `export SPOON_API_KEY` = 'Spoonacular API Key goes here'

Now you must change 2 specific lines in the routes.py file in order to get the code up and running. Line 45 and 59 contains a Heroku link that must be changed to your localhost URL. Change the part of the line containing “https://vast-peak-91474.herokuapp.com” to your local host. DO NOT CHANGE “/authorized” on the line of code. 

This is all of the requirements needed to have this web application running locally. 


## Linting:
pylint: disable=import-error: This error was disabled because it comes from an import statement having trouble successfully importing the specified module. 
  
pylint: disable=broad-except: Used when an except catches a too general exception, possibly burying unrelated errors. This error was present in our flask_test.py file as the exception was “as e”. Trying to catch the exception of “some modules are missing” error. 
  
pylint: disable=consider-using-f-string: Used when a string that is being formatted with format() or % which could potentially be a f-string. This is present in the flask_test.py as format(e).
  
pylint: disable=redefined-outer-name:  Used when a variable's name hides a name defined in the outer scope.This is present in the flask_test.py file.
  
/* eslint-disable react/prop-types */: Disabling because of use of a plugin used that is not recognized. 
  
  
  
