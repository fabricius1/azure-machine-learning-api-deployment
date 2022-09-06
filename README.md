<h1 align="center">Deploy a Dockerized Machine Learning API to Azure App Service using Django Ninja and Terraform</h1>

<br />

## Table of contents

1. [Project description](#project-description)
2. [Installations needed](#installations-needed)
3. [Project structure](#project-structure)
4. [Implementing an R linear regression model in Python with `rpy2`](#implementing-an-r-linear-regression-model-in-python-with-rpy2)
5. [Model update X model info](#model-update-x-model-info)
6. [Installing and running the project](#installing-and-running-the-project)
7. [List of API routes](#list-of-api-routes)
8. [Possible minor issue after accessing the `predict` route for the first time](#possible-minor-issue-after-accessing-the-predict-route-for-the-first-time)
9. [Techs used in this project](#techs-used-in-this-project)

## Project description

This project implements a didactic linear regression model as an API served by Django. The model has only 15 observations, one variable chosen as target (`height`), and its explanatory variable (`weight`). This dataset is available [on this link on Kaggle](https://www.kaggle.com/datasets/tmcketterick/heights-and-weights) and distributed under a [CCO: Public Domain licence](https://creativecommons.org/publicdomain/zero/1.0/).

By analyzing how this simplified ML model API was implemented with Django Ninja, other people can create more complex solutions using this Django module. As a matter of fact, Django Ninja has all the advantages of microframeworks like FastAPI (with a very straightforward functional approach) but also can benefit from the resources already available in the Django ecosystem (admin area, Django's ORM, security measures out of the box, *etc*.). 

## Required installations and signatures to run this project

- Signatures needed:
    - Azure, to deploy the webapp ([students subscription](https://azure.microsoft.com/en-us/free/students/) / [normal subscription](https://azure.microsoft.com/en-us/free/))
    - Docker Hub, to save the docker public image ([sign up here](https://hub.docker.com/signup))
- Programs to have installed on your machine:
    - [Python 3.10](https://www.python.org/downloads/)
    - [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)
    - [Docker CLI](https://docs.docker.com/engine/install/)
    - [Terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli)

## How to run the project
```shell
# Clone this repository
git clone 

# Create a Python virtual environment with venv
python3 -m venv .myenv

# Activate the Python virtual environment
source .myenv/bin/activate

# Install Python extra modules with pip
pip install -r requirements.txt

# Run this command to create the .env file
python3 contrib/setup_env_file.py

# Run this command to create the main.tf terraform file
python3 contrib/setup_terraform_file.py

# Run this command to check the api locally on your computer
# (on your browser, go to http://localhost:8000)
python3 django_project/manage.py runserver

# Build the Docker image
docker build -t <DOCKER_USERNAME>/<DOCKER_IMAGE_NAME> .

# Login to your Docker Hub account
docker login

# Push the Docker image to Docker Hub
docker push <DOCKER_USERNAME_HERE>/<DOCKER_IMAGE_NAME>

# Use Azure CLI to login on your Azure account
az login

# Initialize Terraform
terraform init

# Run this terraform command (An error will be raised):
terraform plan

# The error happened because the docker_image string in main.tf is empty.
# Open main.tf and insert the path to your image saved on Docker Hub
"docker.io/<DOCKER_USERNAME>/<DOCKER_IMAGE_NAME>"

# check if the command works now
terraform plan

# if so, apply the Terraform changes
terraform apply

# Wait a few minutes until the resources are deployed by Azure

# Run this command to get you webapp link or find it on Azure Portal
# (the link will have your webapp name followed by .azurewebsites.net)
az webapp list | jq .[].hostNames

# Finally, open the api deployed to Azure on your browser and test it.
```

## Implementing an R linear regression model in Python with `rpy2`

Although Python has its own OLS model implementations (such as the one in the `statsmodels` package), I decided to use this project as an opportunity to learn the skill of making R models and other resources work together with Python code. Thus, I chose the `rpy2` module to achieve this goal.

Futhermore, by making the two programming languages most used in ML work together when necessary, some interesting new possibilities emerge, such as using the `stepwise procedure` from R to determine which explanatory variables should be kept in a regression model (a resource I have not found yet implemented in Python the way R makes available).

The code for creating/updating the linear regression model with R's `lm()` function can be found in the `django_project/scripts/update_lm.py` file. On the other hand, R's `predict()` function is used in the `django_project/lm_app/api.py` file (inside the `predict` Python function, called when the route `.../lm/api/predict/{weight}` is accessed).

## Model update X model info

This project was structured so that two distinct processes can work independently: the model creation/update, on one hand; and displaying its information and using its predictive functionality, on the other. 

Such separation of concerns is achieved by running the `django_project/scripts/update_lm.py` script, which saves both the R linear model and its information in two different files (`modelr.pickle` and `model_info.json`, respectively) inside the `lm_app/extra_files` folder. 

So, if a model takes hours or days to be generated or updated, one can do that beforehand by running the command:
> `python manage.py runscript update_lm`

When this updating process is done, the resulting files `model_info.json` and `modelr.pickle` from the model's new version will be used by the API when one of its routes is accessed.  

## Project structure

* `contrib`: a folder with only two setup files:
    * `setup_env_file.py`
    * `setup_terraform_file.py`

* `django_project`: folder containing all the Django related files

    * `entrypoint_files`: project folder with the following Django files:
        * `asgi.py`
        * `settings.py`
        * `urls.py`
        * `wsgi.py`

    * `lm_app`: a Django app folder.
        * `extra_files` directory: it was created manually to receive three important files:
            * `data.csv`: dataset used by the Linear Model.
            * `model_info.json`: JSON file with the model information to be displayed in the API routes.
            * `modelr.pickle`: it is the R Linear Model saved as a Python object in a `pickle` file.
            
        * `api.py`: file created manually. It concentrates the API routes to be used by Django Ninja.
        * `urls.py`: file created manually. It imports the Django Ninja API and its routes saved in the `api` variable from the `api.py` file, so they can be included in Django's routes system.
        * `views.py`: file generated by Django whose content is just a short function making the `/lm` route redirect to the API documentation on `/lm/api/docs`.
        * `migrations`, `admin.py`, `apps.py`, `models.py`, and `tests.py`: these files and folder were automatically generated by Django and were not used in this didactic project, even though they probably would in bigger ones. So, I decided to leave them here.

    * `scripts`: a manually created folder containing only one file (`update_lm.py`). This structure is used to run scripts with the `Django Extensions` module.

    * `manage.py`: file generated by Django and entry point for many Django commands.


* other files in the project root:
    * `.gitignore`
    * `Dockerfile`
    * `LICENCE`
    * `README.md`
    * `requirements.txt`

## Technologies used in this project

* Terraform
* Docker
* Microsoft Azure Cloud Provider
* Azure CLI
* Python 3.10.6
* R 4.1.12
* Git and GitHub
* Bash
* Python extra modules:
    * Django
    * Django Ninja
    * Django Extensions
    * python-decouple
    * rpy2
    * venv