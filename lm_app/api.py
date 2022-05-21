from django.http import HttpResponse
from ninja import NinjaAPI
import pickle
import json
import os


api = NinjaAPI()


def generate_filepath(filename):
    return os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'extra_files',
        filename)


def open_json_file(filename):
    with open(filename) as file:
        dictionary = json.load(file)
    
    return dictionary


@api.get('r_squared/')
def get_r_squared(request):
    dct = open_json_file(generate_filepath('model_info.json'))
    return dct['r_squared']


@api.get('adjusted_r_squared/')
def get_adjusted_r_squared(request):
    dct = open_json_file(generate_filepath('model_info.json'))
    return dct['adjusted_r_squared']


@api.get('key/{key}/')
def get_model_info(request, key):
    dct = open_json_file(generate_filepath('model_info.json'))
    if key not in dct:
        return f"Key '{key}' is invalid. Try again."    

    return dct[key]


@api.get('list_keys/')
def list_keys(request):
    dct = open_json_file(generate_filepath('model_info.json'))
    return sorted(list(dct.keys()))


@api.get('predict/{distance}/')
def predict(request, distance: int):
    import rpy2.robjects as robjects
    
    filepath = generate_filepath('modelr.pickle')

    with open(filepath, "rb") as file:
        modelr = pickle.load(file)
        
    # check if prediction doesn't extrapolate the model limits
    distance_values = modelr[-1][1]
    max_distance = max(distance_values)
    min_distance = min(distance_values)
    
    if distance < min_distance or distance > max_distance:
        return HttpResponse(f"Distance can't be lesser than {min_distance}"
                            f" or greater than {max_distance}")
    
    # make prediction
    result = robjects.r.predict(
        modelr,
        robjects.DataFrame({"distance":distance})
    )
    
    return HttpResponse(round(result[0], 6))