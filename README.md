<h1 align="center">Deploy a Dockerized Machine Learning API to Azure App Service using Django Ninja e Terraform</h1>

<br />

# Table of contents

1. [Project description](#project-description)
2. [Installations needed](#installations-needed)
3. [Project structure](#project-structure)
4. [Implementing an R linear regression model in Python with `rpy2`](#implementing-an-r-linear-regression-model-in-python-with-rpy2)
5. [Model update X model info](#model-update-x-model-info)
6. [Installing and running the project](#installing-and-running-the-project)
7. [List of API routes](#list-of-api-routes)
8. [Possible minor issue after accessing the `predict` route for the first time](#possible-minor-issue-after-accessing-the-predict-route-for-the-first-time)
9. [Techs used in this project](#techs-used-in-this-project)

# Project description

This project implements a didactic linear regression model as an API served by Django. The model has only 15 observations, one variable chosen as target (`height`), and it dependent variable (`weight`). This is a Kaggle dataset available [on this link](https://www.kaggle.com/datasets/tmcketterick/heights-and-weights) and distributed under a [CCO: Public Domain licence](https://creativecommons.org/publicdomain/zero/1.0/).

By analyzing how this simplified ML model API was implemented with Django Ninja, other people can create more complex solutions using this Django module. As a matter of fact, Django Ninja has all the advantages of microframeworks like FastAPI (with a very straightforward functional approach) but also can benefit from the resources already available in the Django ecosystem (admin area, Django's ORM, security measures out of the box, *etc*.). 

# Requisited installations and signatures to run this project

- signatures needed:
    - Azure ([students subscription](https://azure.microsoft.com/en-us/free/students/) / [normal subscription](https://azure.microsoft.com/en-us/free/))
    - Docker Hub ([sign up here](https://hub.docker.com/signup))
- Programs to have installed on your machine:
    - [Python 3.10](https://www.python.org/downloads/)
    - [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)
    - [Docker CLI](https://docs.docker.com/engine/install/)
    - [Terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli)

# How to run the project
```shell
# create python virtual env
python3 -m venv .myenv

# activate python virtual env
source .myenv/bin/activate

# install extra modules with pip
pip install -r requirements.txt

# run this command to create the .env and main.tf files
# add a django app name as extra argument if desired
python3 django_code/contrib/setup_env_and_terraform.py

# run this commando to check the api locally on your computer
# (on your browser, go to http://localhost:8000)
python3 django_code/manage.py runserver

# build the docker image
docker build -t <DOCKER_USERNAME>/<DOCKER_IMAGE_NAME> .

# Login to your Docker Hub account
docker login

# push the docker image to docker hub
docker push <DOCKER_USERNAME_HERE>/<DOCKER_IMAGE_NAME>

# use Azure CLI to login on your azure account
az login

# initialize Terraform
terraform init

# Run this terraform command:
terraform plan

# An error will be raised because the docker_image config is empty.
# Open main.rf and insert the path to your Docker image in Docker Hub
"docker.io/<DOCKER_USERNAME>/<DOCKER_IMAGE_NAME>"

# check if the command works now
terraform plan

# if so, apply the terraform changes
terraform apply

# the resources should now be created in you Azure account
```

# Project structure

* `ml_api`: project folder with the following Django files:
    * `asgi.py`
    * `settings.py`
    * `urls.py`
    * `wsgi.py`

<br/>

* `lm_app`: a Django app folder.
    * `extra_files` directory: it was created manually to receive three important files:
        * `model_info.json`: JSON file with the model information to be displayed in the API routes.
        * `modelr.pickle`: it is the R Linear Model saved as a Python object in a `pickle` file.
        * `timedistance.csv`: dataset used by the Linear Model.
    * `api.py`: file created manually. It concentrates the API routes generated by Django Ninja.
    * `apps.py`: file generated by Django and unmodified after that.
    * `urls.py`: file created manually. It imports the Django Ninja API and its routes saved in the `api` variable from the `api.py` file and then includes it in Django's routes system.
    * `views.py`: file generated by Django whose content is just a short function view returning an `<h1>` placeholder for the route `http://localhost:8000/lm`.
    * `migrations`, `admin.py`, `models.py`, and `tests.py`: these files/folder automatically generated by Django were not used in this didactic project, but they probably will be in bigger ones. So, I decided to leave them here.

<br/>

* `scripts`: a manually created folder containing only one file (`update_lm.py`). This structure is demanded to run scripts using the `Django Extensions` module later.

<br />

* files in the project root:
    * `.gitignore`
    * `LICENCE`
    * `README.md`
    * `manage.py`: file generated by Django and entry point for many Django commands.
    * `requirements.txt`: list the Python packages used in this project and their corresponding versions.

# Implementing an R linear regression model in Python with `rpy2`

Although Python has its own OLS model implementations (such as the one in the `statsmodels` package), I decided to use this project as an opportunity to learn the skill of making R models and other resources work together with Python code. Thus, I chose the `rpy2` module to achieve this goal.

Futhermore, by making the two programming languages most used in ML work together when necessary, some interesting new possibilities emerge, such as using the `stepwise procedure` from R to determine which explanatory variables should be kept in a regression model (a resource I have not found yet implemented in Python the way R makes available).

The code for creating/updating the linear regression model with R's `lm()` function can be found in the `scripts/update_lm.py` file. On the other hand, R's `predict()` function is used in the `lm_app/api.py` file (inside the `predict` Python function, called when the route `http//:localhost:8000/lm/api/predict/{distance}` is accessed).

# Model update X model info

This project was structured so that two distinct processes can work independently: the model creation/update, on one hand; and displaying its information and using its predictive functionality, on the other. 

Such separation of concerns is achieved by running the `scripts/update_lm.py` script, which saves both the R linear model and its information in two different files (`modelr.pickle` and `model_info.json`, respectively) inside the `lm_app/extra_files` folder. 

So, if a model takes hours or days to be generated or updated, one can do that beforehand by running the command `python manage.py runscript update_lm`. When this process is done, the resulting files `model_info.json` and `modelr.pickle` from the model's last version will be used by the API when one of its routes is accessed.  

# Installing and running the project

1. Make sure you have both Python and R installed on your machine. I used Python 3.10.2 and R 4.1.2 in this project. Some extra configuration of environmental variables might be necessary due to the *rpy2* module. If that is the case, you can consult [rpy2 official documentation](https://rpy2.github.io/doc/latest/html/introduction.html).

2. Clone this repository in your local machine with `git clone https://github.com/fabricius1/Django-Machine-Learning-API.git`;

3. Create a Python virtual environment, then activate it. For further information about these steps, you can consult [this tutorial](https://github.com/fabricius1/python-virtual-environments), which shows how to create virtual environments with Python's built-in *venv* module;

4. With the virtual environment already activated, install the necessary Python modules:

> ```pip install -r requirements.txt```

5. Start the Django local server in the default `8000` port (or choose another port):

> ```python manage.py runserver```

6. Access `http://localhost:8000/` and `http://localhost:8000/lm` on your browser. If you see the `<h1>` placeholders to these pages, with the messages `Index Page` and `Linear Model Main Page`, respectively, everything is working fine with your API installation.

7. Whenever you want to update the linear regression model (for example, if more observations were added to its database), run the following command:

> ```python manage.py runscript update_lm```

# List of API routes 

1. With the Django server still running, access `http://localhost:8000/lm/api/docs` to check the API Swagger documentation listing all the available routes. You can test them there or access the routes directly.

2. Check the route `http://localhost:8000/lm/api/list_keys` first, which shows all the keys available to be used as parameters in the more general route `http://localhost:8000/lm/api/key/{chosen_key}`. For example, to access the list of fitted values (saved in the `fitted_values` key from the `model_info.json` dictionary), go to the following route:

> ```http://localhost:8000/lm/api/key/fitted_values```

3. The route `http://localhost:8000/lm/api/predict/{distance}`, which utilizes the model predictive functionality, demands the distance be passed as a route parameter. For example, if you want to know what is the predicted time when the distance is 29.5, access the following route:

> ```http://localhost:8000/lm/api/predict/29.5```

4. In the `predict` route, you can pass distances as integers (17 or 28, for example) or floats with either a dot or a comma as decimal separators (either 29.4 or 29,4 would be valid options). However, only distances between 5 and 32 are allowed to avoid model extrapolation. In fact, we can't guarantee that the model would continue behaving in a linear manner below the minimum or above the maximum distance observed in the dataset used to train the model.

# Possible minor issue after accessing the `predict` route for the first time

When the `predict` API route makes a successful prediction, the terminal running Django will keep running. However, one will not be able to stop it from running with CTRL + C anymore. This issue was already identified and reported in the *rpy2* module (more information in https://github.com/rpy2/rpy2/issues/875).

If you run into this problem, close the terminal tab and open a new one.

# Techs used in this project

* Python 3.10.2
* R 4.1.12
* Python modules:
    * Django
    * Django Ninja
    * Django Extensions
    * rpy2
    * venv
