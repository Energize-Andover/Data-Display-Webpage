import pandas as pd
from datetime import datetime
import math
import sys


def get_wing(dataframe, wing):
    wings = pd.read_csv("csv/ahs_air_wing.csv")

    is_in_wing = []
    for i, row in dataframe.iterrows():
        index = get_index_of_value(wings['Label'], row['Location'])
        if index == -1:
            is_in_wing.append(False)  # if the value doesn't exist, it isn't in the wing?
            continue
        is_in_wing.append(str(wings.get_value(index, 'Wing')) == str(wing))
    wing_df = dataframe[is_in_wing]

    return wing_df


def get_index_of_value(series, value):
    if(len(series[series == str(value)].index) == 0):
        return -1
    return series[series == str(value)].index[0] # copied from stackoverflow


def get_floor(dataframe, floor):
    floors = pd.read_csv("csv/ahs_air_wing.csv")

    is_on_floor = []
    for i, row in dataframe.iterrows():
        index = get_index_of_value(floors['Label'], row['Location'])
        if index == -1:
            is_on_floor.append(False) # if the value doesn't exist, it isn't on the floor?
            continue
        is_on_floor.append(float(floors.get_value(index, 'Floor')) == float(floor))
    floor_df = dataframe[is_on_floor]

    return floor_df


def get_series_max(series):
    if series.size == 0:
        return (-1, -1)

    max_val = 0
    for i in series.index:
        if math.isnan(series[i]):
            continue
        max_val = series[i]
        break
    max_index = 0
    index = 0
    for val in series:
        if((val > max_val) and math.isnan(val) == False):
            max_val = val
            max_index = index
        index += 1
    return (max_val, max_index)


def load_data(file):
    df = pd.read_csv(file)
    wings = ["A", "B", "C", "D"]
    floors = [1, 2, 3]
    units = ["Temperature", "CO2"]
    results = [[[[-1, -1, ""]] * 4] * 3] * 2

    # [-1, "", -1] average, room name, max
    # need 3 of above for each floor, and need two of those for temp and co2

    for i, unit in enumerate(units):
        results[i] = list(results[0])
        for j, floor in enumerate(floors):
            results[i][j] = list(results[0][0])
            for k, wing in enumerate(wings):
                data = get_wing(get_floor(df, floor), wing)
                print(data)
                print(data.empty)
                if data.empty:
                    temp = [-1, -1, None]
                else:
                    result = get_series_max(data[unit])
                    if result == (-1, -1):
                        temp = [data[unit].mean(), -1, None]
                    else:
                        rooms = data['Location']
                        room = rooms[rooms.index[result[1]]]
                        temp = [data[unit].mean(), result[0], room]
                results[i][j][k] = list(temp)

    for i, unit in enumerate(units):
        for j, floor in enumerate(floors):
            for k, wing in enumerate(wings):
                for l in range(3):
                    val = results[i][j][k][l]
                    if (type(val) == float and math.isnan(val) or val == -1) or val == 'nan':
                        results[i][j][k][l] = 0
                    if type(val) == float:
                        results[i][j][k][l] = int(results[i][j][k][l] + 0.5)
                    if val == None:
                        results[i][j][k][l] = "No Rooms"
    return results


def update_data(data, new_data, wing_num, floor):
    print("new data ", new_data)
    for i in range(2):
        for j in range(3):
            data[i][floor][wing_num][j] = new_data[i][floor][wing_num][j]
    return data