from django.shortcuts import render
from django.http import HttpResponse
import pickle
import os


def main(request):
    return HttpResponse("<h1>Linear Model Main Page</h1>")


def predict(request, distance):
    import rpy2.robjects as robjects
    
    filepath = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "extra_files",
        "modelr.pickle")

    with open(filepath, "rb") as file:
        modelr = pickle.load(file)
        
    # check prediction doesn't extrapolate the model limits
    distance_values = modelr[-1][1]
    max_distance = max(distance_values)
    min_distance = min(distance_values)
    
    if distance < min_distance or distance > max_distance:
        return HttpResponse(f"Distance can't be lesser than {min_distance}"
                            f" or greater than {max_distance}")
    
    result = robjects.r.predict(
        modelr,
        robjects.DataFrame({"distance":distance})
    )
    
    return HttpResponse(round(result[0], 6))