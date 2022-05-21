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
def predict(request, distance):
    filepath = generate_filepath('modelr.pickle')

    with open(filepath, "rb") as file:
        modelr = pickle.load(file)
        
    # check if prediction doesn't extrapolate the model limits
    distance_values = modelr[-1][1]
    max_distance = max(distance_values)
    min_distance = min(distance_values)
    
    # convert the distance parameter from string to int or float
    try:
        if "," in distance:
            distance = distance.replace(",", ".")
        if "." in distance:
            distance = float(distance)
        else:
            distance = int(distance)
    except:
        return HttpResponse("Either a non numeric value or an invalid numeric"
                            " format was passed as distance. Use integer values"
                            " or float values without thousands separator.")
    
    if distance < min_distance or distance > max_distance:
        return HttpResponse(f"Distance can't be lesser than {min_distance}"
                            f" or greater than {max_distance}")
    
    # This import is strangely placed here to avoid as much as possible the rpy2
    # problem described in https://github.com/rpy2/rpy2/issues/875
    import rpy2.robjects as robjects
    
    # make prediction
    result = robjects.r.predict(
        modelr,
        robjects.DataFrame({"distance":distance})
    )
    
    return HttpResponse(round(result[0], 6))