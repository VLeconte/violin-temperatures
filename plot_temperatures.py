import itertools

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

BIN_SIZE = 1
DATA_FILEPATH = r"C:\Users\vleco\Documents\VincentLeconteCode\violin-temperatures\data\open-meteo-44.80N0.60W16m-1950-2022.csv"


def main():
    df_temperatures = pd.read_csv(
        filepath_or_buffer=DATA_FILEPATH,
        header=2,
    )

    df_temperatures["time"] = df_temperatures["time"].str[:-6]

    df_temperatures = df_temperatures.astype(int)

    all_years = list(
        range(
            min(df_temperatures["time"]),
            max(df_temperatures["time"]) + 1,
            1,
        )
    )

    all_temperatures = list(
        range(
            int(
                np.floor(min(df_temperatures["apparent_temperature_max (°C)"]))
            ),
            int(np.ceil(max(df_temperatures["apparent_temperature_max (°C)"])))
            + 1,
            BIN_SIZE,
        )
    )

    df_temperatures_count = pd.DataFrame(
        {
            "time": pd.Series(all_years).repeat(len(all_temperatures)),
            "apparent_temperature_max (°C)": all_temperatures * len(all_years),
            "count": np.zeros(len(all_temperatures) * len(all_years)),
        }
    )

    for temperature in df_temperatures["apparent_temperature_max (°C)"]:
        temperature = min(
            all_temperatures,
            key=lambda x: abs(x - temperature),
        )

    for time, temperature in itertools.product(all_years, all_temperatures):
        df_temperatures_count["count"] = np.where(
            (df_temperatures_count["time"] == time)
            & (
                df_temperatures_count["apparent_temperature_max (°C)"]
                == temperature
            ),
            len(
                df_temperatures[
                    (df_temperatures["time"] == time)
                    & (
                        df_temperatures["apparent_temperature_max (°C)"]
                        == temperature
                    )
                ]
            ),
            df_temperatures_count["count"],
        )

    plt.figure(figsize=(13, 10), dpi=80)
    for i_year, year in enumerate(all_years):
        plt.barh(
            y=df_temperatures_count.loc[df_temperatures_count["time"] == year][
                "apparent_temperature_max (°C)"
            ],
            width=df_temperatures_count.loc[
                df_temperatures_count["time"] == year
            ]["count"]
            / max(df_temperatures_count["count"]),
            left=i_year
            + 1
            - df_temperatures_count.loc[df_temperatures_count["time"] == year][
                "count"
            ]
            / max(df_temperatures_count["count"])
            / 2,
            color=plt.get_cmap("jet")(
                (np.array(all_temperatures) - min(all_temperatures))
                / (max(all_temperatures) - min(all_temperatures))
            ),
            height=BIN_SIZE,
        )

    plt.title("Horizontal bar plot", fontsize=22)
    plt.show()

    plt.figure(figsize=(13, 10), dpi=80)
    sns.violinplot(
        x="time",
        y="apparent_temperature_max (°C)",
        data=df_temperatures,
        scale="width",
        inner="box",
        density_norm="count",
        common_norm=True,
    )

    # sns.catplot(
    #     data=df_temperatures,
    #     x="time",
    #     hue="apparent_temperature_max (°C)",
    #     kind="count",
    # )

    plt.title("Violin Plot of Highway Mileage by Vehicle Class", fontsize=22)
    plt.show()


if __name__ == "__main__":
    main()
