import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from scipy import stats
from data_import import import_data
import scikit_posthocs as sp


def select_groups():
    parameters = input("Which parameters would you like to examine? \nOptions: Locomotion, OFT, NOR, FST, NSF, EPM, "
                       "Sucrose, Water, or Weight \nType your selections separated by spaces \n")
    split_params = parameters.split()
    num_params = len(split_params)
    message = ""

    if num_params == 1:
        message = "You have selected " + str(num_params) + " parameter: "
    elif num_params > 1:
        message = "You have selected " + str(num_params) + " parameters: "

    for param in split_params:
        if num_params == 1:
            message += param + "."
        elif split_params.index(param) == split_params.index(split_params[-1]):
            message += "and " + param + "parameters."
        else:
            message += param + ", "
    print(message)

    print("-----------------------------------------------------------------------------------------------------------")

    groups = input("Which groups would you like to compare? \nOptions: Non-Stress, Control, 10Hz, 20Hz, 40Hz \nType "
                   "your selections separated by spaces \n")
    split_groups = groups.split()
    num_groups = len(split_groups)

    if num_groups == 2:
        print("You have selected 2 groups. Running Wilcoxon rank sums test on " + split_groups[0] + " and " +
              split_groups[1] + " groups.")

    if num_groups > 2:
        message = "You have selected " + str(num_groups) + " groups. Running Kruskal-Wallis ANOVA with Dunn test for" \
                                                           "post-hoc analysis "
        for group in split_groups:
            if split_groups.index(group) == split_groups.index(split_groups[-1]):
                message += "and " + group + " groups"
            else:
                message += group + ", "
        print(message)

    print("-----------------------------------------------------------------------------------------------------------")

    return [split_params, split_groups]


def run_stats(clean_data, parameters, groups):
    # "grouped" is a GroupBy object containing data from all mice grouped by their experimental treatment
    grouped = clean_data.groupby("condition")

    # "grouped_data" is a list containing the data for the mice in each group in "groups" as each element. For example,
    # if you have selected to compare the mice exposed to 10Hz and 20Hz stimulation, "grouped_data[0]" would contain
    # all data for mice exposed to 10Hz and "grouped_data[1]" would contain all data for mice exposed to 20Hz.
    grouped_data = []
    for group in groups:
        grouped_data += [grouped.get_group(group)]

    for parameter in parameters:
        if len(groups) == 2:
            print("||||||||||||||||||||||||||||")
            print("Results from Wilcoxon rank sums test between selected groups for " + parameter + " parameter:")
            print(stats.ranksums(*grouped_data))
            print("||||||||||||||||||||||||||||")

        elif len(groups) > 2:
            print("||||||||||||||||||||||||||||")
            print("Results from Kruskal-Wallis test between selected groups for " + parameter + " parameter:")
            print(stats.kruskal(*grouped_data))
            print("Result from post-hoc Dunn test between selected groups for " + parameter + " parameter:")
            print(sp.posthoc_dunn(grouped_data, p_adjust="bonferroni"))
            print("||||||||||||||||||||||||||||")

    print("-----------------------------------------------------------------------------------------------------------")


output = select_groups()
path = ""
# run_stats(import_data(path), output[0], output[1])

