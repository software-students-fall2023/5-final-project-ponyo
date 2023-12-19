[![CI/CD](https://github.com/software-students-fall2023/5-final-project-ponyo/actions/workflows/cd-ci.yml/badge.svg)](https://github.com/software-students-fall2023/5-final-project-ponyo/actions/workflows/cd-ci.yml)
# Link to project


# Team Members

`alexh212`- Alex Hmitti

`as13909` - Aaron Stein 

`Rafinator123` - Rafael Nadal-Scala

`jk021227` - Jhon Kim 

# Description

Ponyo Plants is a plant health app that identifies and analyzes a photo of your choice of plant through a machine learning model. 

Using ['Plant.id's plant analysis model'](https://web.plant.id/plant-health-assessment/), the app will first identify with a certain probability the plant that you have uploaded alongside displaying its health percentage. If you upload something that is NOT a plant (is_plant <0.5), it will flash a warning asking you to upload a photo of a valid plant.

# Links
## Link to project
http://167.172.18.107:5001/

## Docker hub repository
https://hub.docker.com/r/rafinator123/ponyo-plants


# Dependencies

Ponyo Plants uses Plant.id's API that require unique keys for access. 
If you do not have a personal Plant.id API key, create an account via (https://admin.kindwise.com/signup?_gl=1*15v4app*_ga*MTgwNDcyMzMyOS4xNzAyNzY2MDkz*_ga_WG5G72QXPW*MTcwMjk0NTQ5OC4yLjEuMTcwMjk0NTU3OC4wLjAuMA..*_ga_YF3JF8EDWW*MTcwMjk0NTQ5OC4yLjEuMTcwMjk0NTU3OC40Ni4wLjA.). 
Then, click on 'Create new API key'. A pop-up window will appear asking for the specifications of creating the API key, make sure to select 'Plant.id', name the API key, and assign the max. number of credits which is 100. Once you do that, copy that API key and place it inside your .env file as API_KEY=(your API key).

Ponyo Plants relies on Docker for containerization - ensure Docker is installed on your machine. 
If not, download and install it [here](https://www.docker.com/products/docker-desktop/).

# Installation

To get started, clone the repository to your local machine and navigate to the project's directory. 

Inside of `5-final-project-ponyo/`, create a `.env` file with the following contents:

```
{
    DATABASE_CONNECTION_STRING=mongodb+srv://ykim021227:gKP6MGYC0lAI96bb@plant.zm0eyo8.mongodb.net/?retryWrites=true&w=majority
    DATABASE_NAME=ponyo_plant
    COLLECTION_NAME=users
    FLASK_SECRET_KEY=ponyoisthestrongestcharacterintheworldandifudisagreeurincorrect1227
    API_KEY=YOUR_API_TOKEN_HERE
}
```
Replace the text `YOUR_API_TOKEN_HERE` with your Plant.id API Key, and save. 

# Usage

Begin the application by running the following command: `docker-compose up --build`

You'll see a series of1`` messages appearing, indicating the progress of the build process.

Once the build process is complete, you should see the following lines, indicating that the application is up and running:

```bash

ponyo-plants  |  * Serving Flask app 'web_app'
ponyo-plants  |  * Debug mode: off
ponyo-plants  | WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
ponyo-plants  |  * Running on all addresses (0.0.0.0)
ponyo-plants  |  * Running on http://127.0.0.1:5001
ponyo-plants  |  * Running on http://172.19.0.3:5001
ponyo-plants  | Press CTRL+C to quit

```

Open `http://127.0.0.1:5001` in your browser and create an account in order to get started. You will NOT be able to access the 'Upload plant' page before creating an account and being logged in. After you have been logged in, click on the 'Upload plant' tab, upload a photo of a plant you want to know the specie and health percentage of.
