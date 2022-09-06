from django.http import HttpResponse
from ninja import NinjaAPI
import pickle
import json
import os


api = NinjaAPI(csrf=True)

def generate_filepath(filename):
    return os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'extra_files',
        filename)


def open_json_file(filename):
    with open(filename) as file:
        dictionary = json.load(file)
    
    return dictionary

@api.get('list_keys/',
         tags = ['Start Here'],
         summary = ('Select one of these keys to use on '
                    'the /model_data/{key}/ route below'))
def list_keys(request):
    dct = open_json_file(generate_filepath('model_info.json'))
    return sorted(list(dct.keys()))


@api.get('model_data/{key}/',
         tags = ['Model Endpoints'],
         summary='Get info about the model by inserting the corresponding key')
def get_model_info(request, key):
    dct = open_json_file(generate_filepath('model_info.json'))
    if key not in dct:
        return f"Key '{key}' is invalid. Try again."    

    return dct[key]




@api.get('predict/{weight}/',
         tags = ['Model Endpoints'])
def predict(request, weight):
    filepath = generate_filepath('modelr.pickle')

    with open(filepath, "rb") as file:
        modelr = pickle.load(file)
        
    # check if prediction doesn't extrapolate the model limits
    weight_values = modelr[-1][1]
    max_weight = max(weight_values)
    min_weight = min(weight_values)
    
    # convert the weight parameter from string to int or float
    try:
        if "," in weight:
            weight = weight.replace(",", ".")
        if "." in weight:
            weight = float(weight)
        else:
            weight = int(weight)
    except:
        return HttpResponse("Either a non numeric value or an invalid numeric"
                            " format was passed as weight. Use integer values"
                            " or float values without thousands separator.")
    
    if weight < min_weight or weight > max_weight:
        return HttpResponse(f"Weight can't be lesser than {min_weight}"
                            f" or greater than {max_weight}")
    
    # This import is strangely placed here to avoid as much as possible the rpy2
    # problem described in https://github.com/rpy2/rpy2/issues/875
    import rpy2.robjects as robjects
    
    # make prediction
    result = robjects.r.predict(
        modelr,
        robjects.DataFrame({"weight":weight})
    )
    
    return HttpResponse(round(result[0], 6))