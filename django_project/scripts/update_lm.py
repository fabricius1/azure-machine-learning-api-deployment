import rpy2.robjects as ro
import pickle
import json
import os


def run():
    # decimal places to use in rounding operations
    decimal_places = 6

    # create R dataframe
    path = os.path.join("lm_app","extra_files")
    csv_file = os.path.join(path, "data.csv")
    data = ro.r["read.table"](csv_file, sep=",", header=True)

    # formula as Python string
    formula_as_py_str = "height ~ weight"

    # generate linear model
    modelr = ro.r.lm(ro.Formula(formula_as_py_str), data)

    # start an empty dictionary for the future json file
    dct = {}

    # save R summary object
    summary_object = ro.r.summary(modelr)

    # save LM summary call as a Python string
    call = str(ro.r.print(summary_object))
    text = (f"Call:\nlm(formula = {formula_as_py_str}, data = data)"
            f"\n\nResiduals:\n" +
            call.split("\n\nResiduals:\n")[1])
        
    # add summary call to dictionary
    dct["call"] = text

    # add intercept and coeficient
    dct["intercept"] = round(modelr[0][0], decimal_places)
    dct["coef"] = round(modelr[0][1], decimal_places)

    # add residuals
    dct["residuals"] = [round(x, decimal_places) for x in list(modelr[1])]

    # add fitted_values
    dct["fitted_values"] = [round(x, decimal_places) for x in list(modelr[4])]

    # add time and distance variables in the dictionary as lists
    dct["height_values"] = [x for x in list(modelr[-1][0])]
    dct["weight_values"] = [x for x in list(modelr[-1][1])]

    # add observations from dataframe as Python list of lists
    dct["observations"] = [list(x) for x in zip(dct["height_values"], dct["weight_values"])]

    # add r squared statistics 
    dct["r_squared"] = round(summary_object[7][0], decimal_places)
    dct["adjusted_r_squared"] = round(summary_object[8][0], decimal_places)
    
    # add equation:
    dct["equation"] = f'{dct["intercept"]} + {dct["coef"]} * weight'

    # create a json file with the model info dictionary
    json_file = os.path.join(path, "model_info.json")
    with open(json_file, 'w') as file:
        json.dump(dct, file)

    # save the R model into a pickle file
    pickle_file = os.path.join(path, "modelr.pickle")
    with open(pickle_file, "wb") as file:
        pickle.dump(modelr, file)
        
    print("\n\nEnd of Script\n\n")
