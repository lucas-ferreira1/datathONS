import csv
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# Chooses the special day to be analyzed
special_day = "Jogos da Copa"

special_index = 4
date_index = 2

# Maps the days when these special days occur
dates = set()
with open("databases/dados_diaespecial.csv", "r") as file:
    csv_reader = csv.reader(file)
    headers = next(csv_reader)

    for row in csv_reader:
        row = row[0].split(";")
        if row[special_index] == special_day:
            dates.add(row[date_index])

# Opens the charge dataset

with open("databases/dados_carga.csv", "r") as file:
    csv_reader = csv.reader(file)
    headers = next(csv_reader)


# Finds the index of a date in a given dates array
def binary_search(dates: np.ndarray, target_date: str):
    left = 0
    right = len(dates) - 1

    while left <= right:
        mid = (left + right) // 2
        if dates[mid] == target_date:
            return mid  # Found the target date
        elif dates[mid] < target_date:
            left = mid + 1
        else:
            right = mid - 1

    # If the target date is not found in the list, return -1
    return -1
