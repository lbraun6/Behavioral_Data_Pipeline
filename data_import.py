import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from parameter_calculation import calculate_epm, calculate_locomotion, calculate_nor, calculate_nsf, calculate_oft, \
    calculate_fst, calculate_water_consumption, calculate_sucrose_consumption, calculate_body_weight, \
    calculate_social_interaction

# This script takes raw output files for rodent behavioral tasks from Noldus Ethovision, extracts the relevant
# information for the calculation of standard behavioral parameters, and compiles it into a Microsoft Excel file for
# further analysis and visualization.


def import_data():
    path = input(r"Enter the path of the folder containing all of the cohort folders that contain all of the "
                 r"behavioral files you wish to analyze: ")
    folders = os.listdir(path)

    cohort_column = []
    bw_column = []
    locomotion_column = []
    oft_column = []
    nor_column = []
    nsf_column = []
    epm_column = []
    fst_column = []
    social_interaction_column = []
    sucrose_column = []
    water_column = []
    print(folders)

    for folder in folders:
        files = os.listdir(path + "\\" + folder)
        cohort_column += [folder]
        print(files)

        for file in files:
            if file.find("Body Weight") >= 0:
                bw_column += [calculate_body_weight(path + "\\" + folder, file)]
            if file.find("OFT") >= 0:
                locomotion_column += [calculate_locomotion(path + "\\" + folder, file)]
            if file.find("OFT") >= 0:
                oft_column += [calculate_oft(path + "\\" + folder, file)]
            if file.find("NOR") >= 0:
                nor_column += [calculate_nor(path + "\\" + folder, file)]
            if file.find("NSF") >= 0:
                nsf_column += [calculate_nsf(path + "\\" + folder, file)]
            if file.find("EPM") >= 0:
                epm_column += [calculate_epm(path + "\\" + folder, file)]
            if file.find("FST") >= 0:
                fst_column += [calculate_fst(path + "\\" + folder, file)]
            if file.find("Social Interaction") >= 0:
                social_interaction_column += [calculate_social_interaction(path + "\\" + folder, file)]
            if file.find("Sucrose") >= 0:
                sucrose_column += [calculate_sucrose_consumption(path + "\\" + folder, file)]
            if file.find("Sucrose") >= 0:
                water_column += [calculate_water_consumption(path + "\\" + folder, file)]

        for column in [bw_column, locomotion_column, oft_column, nor_column, nsf_column, epm_column, fst_column,
                       social_interaction_column, sucrose_column, water_column]:
            if len(cohort_column) > len(column):
                column += [np.NaN]

    clean_data = pd.DataFrame({

        "bw": bw_column,
        "locomotion": locomotion_column,
        "oft": oft_column,
        "nor": nor_column,
        "nsf": nsf_column,
        "epm": epm_column,
        "fst": fst_column,
        "social interaction": social_interaction_column,
        "sucrose": sucrose_column,
        "water": water_column})

    print(clean_data)
    return clean_data


import_data()
# C:\Users\Luke\Desktop\College\Research\Dr. Franklin\Behavioral Data Pipeline\Flicker Behavior All Frequencies
