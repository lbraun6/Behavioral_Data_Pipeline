import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os


# Done
def calculate_locomotion(path, file):
    raw_data = pd.read_excel(path + "\\" + file, index_col=1, header=0, sheet_name="Analysis")
    split_file = file.split()
    locomotion_frame = {"Mouse": [], "Condition": [], "Distance moved (cm)": []}
    for mouse in range(len(raw_data.index)):
        if mouse > 2:
            locomotion_frame["Mouse"] += [raw_data.index[mouse]]
            locomotion_frame["Distance moved (cm)"] += [raw_data["Distance moved"][mouse]]
            locomotion_frame["Condition"] += [raw_data["Unnamed: 0"][mouse]]

    locomotion_frame = pd.DataFrame(locomotion_frame)
    locomotion_frame.to_csv(path + "\\" + split_file[-3] + " " + split_file[-2] + " " + split_file[-1][0] +
                            " Locomotion Data.csv", index=False)
    return locomotion_frame


# Done
def calculate_oft(path, file):
    raw_data = pd.read_excel(path + "\\" + file, index_col=1, header=0, sheet_name="Analysis")
    split_file = file.split()
    oft_frame = {"Mouse": [], "Condition": [], "Cumulative duration in center (s)": []}
    for mouse in range(len(raw_data.index)):
        if mouse > 2:
            oft_frame["Mouse"] += [raw_data.index[mouse]]
            oft_frame["Condition"] += [raw_data["Unnamed: 0"][mouse]]
            oft_frame["Cumulative duration in center (s)"] += [raw_data["In zone 2.1"][mouse]]

    oft_frame = pd.DataFrame(oft_frame)
    oft_frame.to_csv(path + "\\" + split_file[-3] + " " + split_file[-2] + " " + split_file[-1][0] + " OFT Data.csv", index=False)

    return oft_frame


# Done
def calculate_epm(path, file):
    raw_data = pd.read_excel(path + "\\" + file, index_col=1, header=[0, 1, 2, 3], sheet_name="Analysis")
    split_file = file.split()
    epm_frame = {"Mouse": [], "Condition": [], "Cumulative duration in closed arm (s)": []}
    for mouse in range(len(raw_data.index)):
        if mouse > 2:
            if raw_data["In zone", "Closed arms / Center-point", "Cumulative Duration", "s"][mouse] > 0:
                epm_frame["Mouse"] += [raw_data.index[mouse]]
                epm_frame["Condition"] += [raw_data["Unnamed: 0_level_0", "Unnamed: 0_level_1", "Unnamed: 0_level_2",
                                                    "Unnamed: 0_level_3"][mouse]]
                epm_frame["Cumulative duration in closed arm (s)"] += [raw_data["In zone", "Closed arms / Center-point",
                                                                                "Cumulative Duration", "s"][mouse]]

    epm_frame = pd.DataFrame(epm_frame)
    epm_frame.to_csv(path + "\\" + split_file[-3] + " " + split_file[-2] + " " + split_file[-1][0] + " EPM Data.csv", index=False)

    return epm_frame


# NOT Done
def calculate_nor(path, file):
    raw_data = pd.read_excel(path + "\\" + file, index_col=1, header=[0, 1, 2, 3], sheet_name="Analysis")
    raw_data.dropna(how="all", inplace=True)
    split_file = file.split()
    nor_frame = {"Mouse": [], "Condition": [], "Cumulative duration with object 1 (s)": [],
                 "Cumulative duration with object 2 (s)": []}

    for column in raw_data.columns:
        column = list(column)
        new_col = list(column)
        new_col[1] = new_col[1].replace("Novel cumulative 1.2", "object 1.0")
        new_col[1] = new_col[1].replace("Familiar cumulative 1.2", "object 2.0")
        new_col[1] = new_col[1].replace("Novel cumulative 1", "object 1")
        new_col[1] = new_col[1].replace("Familiar cumulative 1", "object 2")
        raw_data.rename(columns={column[1]: new_col[1]}, inplace=True)

    raw_data["Unnamed: 4_level_0", "Unnamed: 4_level_1", "Unnamed: 4_level_2", "Unnamed: 4_level_3"].replace(
        "For Center-point in Novel cumulative 1.2", "For Nose-point in object 1.0", inplace=True)
    raw_data["Unnamed: 4_level_0", "Unnamed: 4_level_1", "Unnamed: 4_level_2", "Unnamed: 4_level_3"].replace(
        "For Center-point in Familiar cumulative 1.2", "For Nose-point in object 2.0", inplace=True)
    raw_data["Unnamed: 4_level_0", "Unnamed: 4_level_1", "Unnamed: 4_level_2", "Unnamed: 4_level_3"].replace(
        "For Nose-point in Novel cumulative 1.2", "For Nose-point in object 1", inplace=True)
    raw_data["Unnamed: 4_level_0", "Unnamed: 4_level_1", "Unnamed: 4_level_2", "Unnamed: 4_level_3"].replace(
        "For Nose-point in Familiar cumulative 1.2", "For Nose-point in object 2", inplace=True)

    for mouse in raw_data.index:
        for trial in range(len(raw_data["Unnamed: 4_level_0", "Unnamed: 4_level_1", "Unnamed: 4_level_2",
                                        "Unnamed: 4_level_3"][mouse])):

            if raw_data["Unnamed: 4_level_0", "Unnamed: 4_level_1", "Unnamed: 4_level_2",
                        "Unnamed: 4_level_3"][mouse][trial].find("Nose-point") >= 0:

                if mouse not in nor_frame["Mouse"]:

                    print()
                    nor_frame["Mouse"] += [mouse]
                    nor_frame["Condition"] += [raw_data["Unnamed: 0_level_0", "Unnamed: 0_level_1",
                                                        "Unnamed: 0_level_2", "Unnamed: 0_level_3"][mouse][trial]]

                if raw_data["Unnamed: 4_level_0", "Unnamed: 4_level_1", "Unnamed: 4_level_2",
                            "Unnamed: 4_level_3"][mouse][trial].find("1") >= 0:

                    nor_frame["Cumulative duration with object 1 (s)"] += [
                        raw_data["In zone", "object 1 / Nose-point", "Cumulative Duration", "s"][mouse][trial]]

                elif raw_data["Unnamed: 4_level_0", "Unnamed: 4_level_1", "Unnamed: 4_level_2",
                              "Unnamed: 4_level_3"][mouse][trial].find("2") >= 0:

                    nor_frame["Cumulative duration with object 2 (s)"] += [
                        raw_data["In zone", "object 2 / Nose-point", "Cumulative Duration", "s"][mouse][trial]]

    print(nor_frame)
    print(len(nor_frame["Mouse"]))
    print(len(nor_frame["Condition"]))
    print(len(nor_frame["Cumulative duration with object 1 (s)"]))
    print(len(nor_frame["Cumulative duration with object 2 (s)"]))
    nor_frame = pd.DataFrame(nor_frame)
    nor_frame.to_csv(path + "\\" + split_file[-3] + " " + split_file[-2] + " " + split_file[-1][0] + " NOR Data.csv",
                     index=False)
    return nor_frame


# Done
def calculate_social_interaction(path, file):
    raw_data = pd.read_excel(path + "\\" + file, index_col=1, header=[0, 1, 2, 3], sheet_name="Analysis")
    split_file = file.split()
    social_interaction_frame = {"Mouse": [], "Condition": [], "Cumulative duration in center chamber (s)": [],
                                "Cumulative duration in left chamber (s)": [],
                                "Cumulative duration in right chamber (s)": []}
    for mouse in range(len(raw_data.index)):
        if raw_data.index[mouse] not in social_interaction_frame["Mouse"]:
            social_interaction_frame["Mouse"] += [raw_data.index[mouse]]
            social_interaction_frame["Condition"] += [raw_data["Unnamed: 0_level_0", "Unnamed: 0_level_1",
                                                               "Unnamed: 0_level_2", "Unnamed: 0_level_3"][mouse]]

        if raw_data["Unnamed: 3_level_0", "Unnamed: 3_level_1", "Unnamed: 3_level_2", "Unnamed: 3_level_3"][mouse]\
                == "For Nose-point in Center chamber":
            social_interaction_frame["Cumulative duration in center chamber (s)"] += \
                [raw_data["In chambers", "Center chamber / Center-point", "Cumulative Duration", "s"][mouse]]

        elif raw_data["Unnamed: 3_level_0", "Unnamed: 3_level_1", "Unnamed: 3_level_2", "Unnamed: 3_level_3"][mouse]\
                == "For Nose-point in Left chamber":
            social_interaction_frame["Cumulative duration in left chamber (s)"] += \
                [raw_data["In chambers", "Left chamber / Center-point", "Cumulative Duration", "s"][mouse]]

        elif raw_data["Unnamed: 3_level_0", "Unnamed: 3_level_1", "Unnamed: 3_level_2", "Unnamed: 3_level_3"][mouse]\
                == "For Nose-point in Right chamber":
            social_interaction_frame["Cumulative duration in right chamber (s)"] += \
                [raw_data["In chambers", "Right chamber / Center-point", "Cumulative Duration", "s"][mouse]]

    social_interaction_frame = pd.DataFrame(social_interaction_frame)
    social_interaction_frame.to_csv(path + "\\" + split_file[-3] + " " + split_file[-2] + " " + split_file[-1][0] +
                                    " Social Interaction Data.csv", index=False)
    return social_interaction_frame


def calculate_sucrose_consumption(path, file):
    raw_data = pd.read_excel(path + "\\" + file, index_col=2, skiprows=0, sheet_name="Sucrose consumption")
    split_file = file.split()
    sucrose_consumption_frame = {"Mouse": [], "Condition": [], }
    for mouse in range(len(raw_data.index)):
        if raw_data.index[mouse] not in sucrose_consumption_frame["Mouse"]:
            sucrose_consumption_frame["Mouse"] += [raw_data.index[mouse]]
            sucrose_consumption_frame["Condition"] += "n"

    sucrose_consumption_frame = pd.DataFrame(sucrose_consumption_frame)
    sucrose_consumption_frame.to_csv(path + "\\" + split_file[-3] + " " + split_file[-2] + " " + split_file[-1][0] +
                                     " Sucrose Consumption Data.csv", index=False)
    return sucrose_consumption_frame


def calculate_water_consumption(path, file):
    a = "A"


# Done
def calculate_fst(path, file):
    raw_data = pd.read_excel(path + "\\" + file)
    split_file = file.split()
    fst_frame = {"Mouse": [], "Condition": [], "Time spent in immobility (s)": []}
    for mouse in range(len(raw_data["ID"])):
        if not str(raw_data["MOBILITY TIME (min)"][mouse]) == "nan":
            fst_frame["Mouse"] += [raw_data["ID"][mouse]]
            fst_frame["Condition"] += [raw_data["GROUP"][mouse]]
            mobility = str(raw_data["MOBILITY TIME (min)"][mouse])
            split_mobility = mobility.split(":")
            immobility = 240 - ((int(split_mobility[0]) * 60) + int(split_mobility[1]))
            fst_frame["Time spent in immobility (s)"] += [immobility]

    fst_frame = pd.DataFrame(fst_frame)
    fst_frame.to_csv(path + "\\" + split_file[-3] + " " + split_file[-2] + " " + split_file[-1][0] + " FST Data.csv",
                     index=False)
    return fst_frame


def calculate_body_weight(path, file):
    raw_data = pd.read_excel(path + "\\" + file, index_col=1)
    body_weight_frame = {"Mouse": [], "Condition": [], "Cumulative duration in center (s)": []}
    for mouse in raw_data.index:
        body_weight_frame["Mouse"] += [mouse]
        body_weight_frame["Condition"] += [raw_data["Unnamed: 0"][mouse]]
        body_weight_frame["Cumulative duration in center (s)"] += [raw_data["In zone 2.1"][mouse]]

    return body_weight_frame


def calculate_nsf(path, file):
    raw_data = pd.read_excel(path + "\\" + file, index_col=1)
    nsf_frame = {"Mouse": [], "Condition": [], "Cumulative duration in center (s)": []}
    for mouse in raw_data.index:
        nsf_frame["Mouse"] += [mouse]
        nsf_frame["Condition"] += [raw_data["Unnamed: 0"][mouse]]
        nsf_frame["Cumulative duration in center (s)"] += [raw_data["In zone 2.1"][mouse]]

    return nsf_frame


