<h1 align="center">Machine Learning API example with Django Ninja</h1>

<br />

# Table of Contents

# Project Description

This project implements a didactic Linear Regression model as an API served by Django. The model has only ten observation, one explanatory variable (`distance`), its dependent/target variable (`time`), and was taken from the following book (which I strongly recommend for those interested in learning more about ML and Statistics in general):

> FÁVERO, Luiz Paulo; BELFIORE, Patrícia. *Data Science for Business and Decision Making*. 1st Edition. Elsevier Academic Press: *sine loco*, 2019. p.445 (read in the [Kindle Edition](https://www.amazon.com/-/pt/dp/B07QQBDTY1/ref=sr_1_1?__mk_pt_BR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=GJD6R2CGXLTM&keywords=data+science+for+business+and+decision+making+Favero&qid=1653134980&sprefix=data+science+for+business+and+decision+making+favero%2Caps%2C211&sr=8-1))

By analyzing how this simplified ML model API was implemented with Django Ninja, other people can create more complex solutions using this fantastic Django module. As a matter of fact, Django Ninja has all the advantages of microframeworks like FastAPI (with a very straightforward functional approach), but also can benefit from the amazing resources already available in the Django ecosystem (admin area, Django's ORM, security measures out of the box *etc*)

# Project Structure

* `ml_api`: project folder with the following Django files:
    * `asgi.py`
    * `settings.py`
    * `urls.py`
    * `wsgi.py`

<br/>

* `lm_app`: a Django app folder.
    * `extra_files` directory: it was created manually to receive three important files:
        * `model_info.json`: json file with model information to be displayed in the API routes
        * `modelr.pickle`: it is the R Linear Model saved as a Python object in a `pickle` file
        * `timedistance.csv`: dataset used by the Linear Model.
    * `api.py`: file created manually. It concentrates the API routes generated by Django Ninja
    * `apps.py`: file generated by Django and unmodified after that
    * `urls.py`: file created manually. It imports the Django Ninja API and its routes saved in the `api` variable from the `api.py` file and then include it in Django's routes system.
    * `views.py`: file generated by Django whose content is just a short function view returning an `<h1>` placeholder for the route `http://localhost:8000/lm`.
    * `migrations`, `admin.py`, `models.py`, and `tests.py`: these files/folder automatically generated by Django were not used in this didactic project, but they probably will be in bigger ones. So, I decided to leave them here.

<br/>

* `scripts`: a manually created folder that contains only one file (`update_lm.py`). This structure is demanded to run scripts using the `django extensions` module later.

<br />

* files in the project root:
    * `.gitignore`
    * `LICENCE`
    * `README.md`
    * `manage.py`: file generated by Django and entry point for many Django commands.
    * `requirements.txt`: list the Python packages used in this project and their corresponding versions.

# Implementing an R Regression Model in Python with `rpy2`

Although Python has its own OLS model implementations (such as the one in the *statsmodels* package), I decided to use this project as an opportunity to learn the skill of making R models and other resources work together with Python code. Thus, I chose the `rpy2` module to achieve this goal. By making the two programming languages most used in ML work together when necessary, some interesting new possibilities emerge, such as using the `stepwise procedure` from R to determine which explanatory variables should be kept in a Regression Model (a resource I have not found yet implemented in Python the way R makes available).

The code for creating/updating the Linear Regression model with R's `lm()` function can be found in the `scripts/update_lm.py` file. On the other hand, R's `predict()` function is used in the `lm_app/api.py` file (inside the `predict` Python function, called when the route `http:localhost:8000/lm/api/predict/{distance}` is accessed).

# Model Update X Model Info

This project was structured so that two very distinct processes can work independently: the model creation/update, by one hand; and displaying its information and using its predictive functionality, on the other. 

Such "separation of concerns" is achieved by running the `scripts/update_lm.py` script, which saves both the R linear model and its informations in two different files (`modelr.pickle` and `model_info.json`, respectively) inside the `lm_app/extra_files` folder. 

So, if a model takes hours or days to be generated or updated, one can do that beforehand, by running the command `python manage.py runscript update_lm`. When this process is done, the resulting two files `model_info.json` and `modelr.pickle` from the models last version will be used by the API when one of its routes is accessed.  

# Installing and Running the Project

1. Make sure you have both Python and R installed in your machine. I used Python 3.10.2 and R 4.1.2 in this project. Some extra configuration of environmental variables might be necessary due to the *rpy2* module. If that is the case, you can consult [*rpy2* oficial documentation](https://rpy2.github.io/doc/latest/html/introduction.html) or google for solutions.

2. Clone this repository in your local machine with `git clone https://github.com/fabricius1/Django-Machine-Learning-API.git`;

3. Create a Python virtual environment, then activate it. For further information about these steps, you can consult [this tutorial](https://github.com/fabricius1/python-virtual-environments), which shows how to create virtual environments with Python's built-in *venv* module;

4. With the virtual environment already activated, install the necessary Python modules:

```pip install -r requirements.txt```

5. Start the Django local server in the default `8000` port (or choose another port):

```python manage.py runserver```

6. Access `http://localhost:8000/` and `http://localhost:8000/lm`. If you see the `<h1>` placeholders to these pages, with the messages `Index Page` and `Linear Model Main Page`, respectively, that means that everything is working fine with your API installation.

7. Whenever you want to update the Linear Regression model (for example, if more observations were added to it), run the script with the following command:

```python manage.py runscript update_lm```

# List of API Routes 

1. With the Django server still running, access `http://localhost:8000/lm/api/docs` to check the API Swagger documentation listing all available routes. You can test them there or access the routes directly.

2. Check the route `http://localhost:8000/lm/api/list_keys` first, which shows all the keys available to be used as parameters in the more general route `http://localhost:8000/lm/api/key/{chosen_key}`. For example, to access the list of fitted values (saved in the `fitted_values` key, from the `model_info.json` dictionary), go to the following route:

```http://localhost:8000/lm/api/key/fitted_values```

3. The route `http://localhost:8000/lm/api/predict/{distance}`, which utilizes the model predictive functionality, demands that the distance be passed as a route parameter. For example, if you want to know what is the predicted time, when the distance is 29.5, access the following route:

```http://localhost:8000/lm/api/predict/29.5```

4. In the `predict` route, you can pass distances as integers (17, 28 *etc*), floats with either a dot or a comma as decimal separators (29.4 and 29,4 are both valid). However, only distances between 5 and 32 are allowed to avoid model extrapolation. The reason for that is that we can't garantee that the model would continue behaving in a linear manner below or above the minimum and maximum distances observed in the dataset used to train it.

