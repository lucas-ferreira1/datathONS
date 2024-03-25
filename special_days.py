import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import copy
from datetime import datetime, time
import warnings

warnings.filterwarnings("ignore")  # Remove


def main(special_day: str) -> np.ndarray:
    """
    Determines the historical average behavior of the liquid global charge, for the special_day
    considered

    :param special_day: Special_day for which the function is calculated.
    """
    # Reads the database
    file = "databases/dados_carga_diasespeciais.xlsx"

    print("Reading file...")
    df = pd.read_excel(file)
    print(f"Ok. {len(df)} data points have been read.")

    ### df Treatment ###

    # Only keeps the south east region
    df = df[df["cod_areacarga"] == "SECO"]
    df.drop(columns=["cod_areacarga"], inplace=True)

    # Removes extra spaces, and converts dates to datetime
    df["Data especial"] = df["Data especial"].str.strip()
    df["din_referenciautc"] = pd.to_datetime(df["din_referenciautc"])

    # Converts numbers to proper format
    df.iloc[:, [1, 2, 3, 4, 5, 6, 7, 8]] = df.iloc[:, [1, 2, 3, 4, 5, 6, 7, 8]].astype(
        str
    )

    df.iloc[:, [1, 2, 3, 4, 5, 6, 7, 8]] = (
        df.iloc[:, [1, 2, 3, 4, 5, 6, 7, 8]]
        .applymap(lambda x: x.replace(",", "."))
        .astype(float)
    )

    df_special = df[df["Data especial"] == special_day]

    # Group the DataFrame by day
    grouped = df_special.groupby(df_special["din_referenciautc"].dt.date)

    # Create a dictionary to store the DataFrames
    dfs_by_day = []

    # Iterate over the groups and store each DataFrame in the list
    for day, group_df in grouped:
        dfs_by_day.append(group_df)

    adjusted_dfs_by_day = []
    tol = 45

    for df_day in dfs_by_day:
        if df_day.shape[0] == 48:
            df_day.index = range(1, len(df_day) + 1)
            adjusted_dfs_by_day.append(df_day)
        elif df_day.shape[0] >= tol:
            # Repeat the first row of the DataFrame twice
            new_values = pd.concat([df_day.iloc[[0]]] * (48 - df_day.shape[0]))
            # Concatenate the new values with the original DataFrame
            df_day = pd.concat([new_values, df_day])
            df_day.index = range(1, len(df_day) + 1)
            adjusted_dfs_by_day.append(df_day)

    # Calculates the mean values
    df_concat = pd.concat(adjusted_dfs_by_day)

    by_row_index = df_concat.groupby(df_concat.index)
    df_means = by_row_index.mean()

    # Corrects time shift
    delta_t = -3
    carga_global_media = np.roll(np.array(df_means["val_cargaglobal"]), delta_t)

    fig, ax = plt.subplots()
    x_ax = [x / 2 for x in range(48)]
    ax.plot(x_ax, carga_global_media)

    plt.title(f"Global liquid power: {special_day}")
    plt.xlabel("Time (h)")
    plt.ylabel("Power (MW)")
    plt.grid()

    plt.show()

    return carga_global_media


def same_day(x: datetime, y: datetime) -> bool:
    """
    Returns True if x and y are in the same day, and False if not
    """
    try:
        if x.day == y.day and x.month == y.month and x.year == y.year:
            return True
        else:
            return False
    except:
        return False


if __name__ == "__main__":
    special_day = "Carnaval"
    print(f"Special Day: {special_day}")
    print(main(special_day=special_day))
