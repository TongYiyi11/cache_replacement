import os
import matplotlib.pyplot as plt
import pandas as pd
import altair as alt
import numpy as np

alt.renderers.enable('altair_viewer')


def read_result(directory, filename):
    path = os.path.join(directory, filename)
    with open(path) as f:
        for line in f:
            if line.startswith("Finished CPU"):
                data = line.split(" ")
                ipc = data[9]
    return float(ipc)


def read_result_multicore(directory, filename):
    path = os.path.join(directory, filename)
    ipc_lis = [0]*4
    with open(path) as f:
        for line in f:
            if line.startswith("Finished CPU"):
                data = line.split(" ")
                index = int(data[2])
                ipc_lis[index] = float(data[9])
    return ipc_lis


def get_tracelis(directory):
    tracelis = []
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            arr = filename.split("-")
            if multicore == 1:
                trace = arr[0]
            else:
                trace = arr[0].split(".")[0]
            if trace in tracelis:
                continue
            tracelis.append(trace)
    return tracelis


def plot_data(lru_map, ship_map, myrepl_map):
    df = pd.DataFrame([lru_map, ship_map, myrepl_map], index=["lru", "ship", "myrepl"]).transpose()
    fig, ax = plt.subplots(1, 1, figsize=(6, 5))
    df.plot.bar(ax=ax, fontsize=12, rot=0, color={"lru": [152 / 255.0, 223 / 255.0, 238 / 255.0],
                                                  "ship": [114 / 255.0, 158 / 255.0, 206 / 255.0],
                                                  "myrepl": [173 / 255.0, 139 / 255.0, 201 / 255.0]})
    fig.tight_layout()
    fig.show()


def prep_df(df, name):
    df = df.stack().reset_index()
    df.columns = ['c1', 'c2', 'values']
    df['DF'] = name
    return df


def plot_data_multicore(lru_map_lis, ship_map_lis, myrepl_map_lis, tracelis):
    # prepare df
    df0 = pd.DataFrame([lru_map_lis[0], ship_map_lis[0], myrepl_map_lis[0]],
                       index=["lru", "ship", "myrepl"]).transpose()
    df1 = pd.DataFrame([lru_map_lis[1], ship_map_lis[1], myrepl_map_lis[1]],
                       index=["lru", "ship", "myrepl"]).transpose()
    df2 = pd.DataFrame([lru_map_lis[2], ship_map_lis[2], myrepl_map_lis[2]],
                       index=["lru", "ship", "myrepl"]).transpose()
    df3 = pd.DataFrame([lru_map_lis[3], ship_map_lis[3], myrepl_map_lis[3]],
                       index=["lru", "ship", "myrepl"]).transpose()

    df0 = prep_df(df0, 'Core1')
    df1 = prep_df(df1, 'Core2')
    df2 = prep_df(df2, 'Core3')
    df3 = prep_df(df3, 'Core4')

    df = pd.concat([df0, df1, df2, df3])

    # Plot data with Altair
    chart = alt.Chart(df).mark_bar().encode(
        # tell Altair which field to group columns on
        x=alt.X('c2:N', title=None),

        # tell Altair which field to use as Y values and how to calculate
        y=alt.Y('sum(values):Q',
                axis=alt.Axis(
                    grid=False,
                    title=None)),

        # tell Altair which field to use to use as the set of columns to be  represented in each group
        column=alt.Column('c1:N', title=None),

        # tell Altair which field to use for color segmentation
        color=alt.Color('DF:N',
                        scale=alt.Scale(
                            range=['#FFCC99', '#FFCCCC', '#FF9999', '#FF6666'],   # color
                        ),
                        )) \
        .configure_view(
        # remove grid lines around column clusters
        strokeOpacity=0
    ).configure_axis(
        labelFontSize=15,
        titleFontSize=15,
    )
    chart.show()


if __name__ == "__main__":

    directory = "./results_10M/"
    multicore = 0

    # list of trace data name
    tracelis = get_tracelis(directory)
    tracelis.sort()

    # initialization
    if multicore == 1:
        lru_map_lis = []
        ship_map_lis = []
        myrepl_map_lis = []
        for i in range(0, 4):
            lru_map_lis.append(dict.fromkeys(tracelis, 0))
            ship_map_lis.append(dict.fromkeys(tracelis, 0))
            myrepl_map_lis.append(dict.fromkeys(tracelis, 0))
    else:
        lru_map = dict.fromkeys(tracelis, 0)
        ship_map = dict.fromkeys(tracelis, 0)
        myrepl_map = dict.fromkeys(tracelis, 0)

    # read data
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            arr = filename.split("-")
            if multicore == 1:
                trace = arr[0]
            else:
                trace = arr[0].split(".")[0]
            algo = arr[-2]
            if multicore == 1:
                ipc = read_result_multicore(directory, filename)
                if algo == "lru":
                    for i in range(0, 4):
                        lru_map_lis[i][trace] = ipc[i]
                elif algo == "ship":
                    for i in range(0, 4):
                        ship_map_lis[i][trace] = ipc[i]
                elif algo == "myrepl":
                    for i in range(0, 4):
                        myrepl_map_lis[i][trace] = ipc[i]
            else:
                ipc = read_result(directory, filename)
                if algo == "lru":
                    lru_map[trace] = ipc
                elif algo == "ship":
                    ship_map[trace] = ipc
                elif algo == "myrepl":
                    myrepl_map[trace] = ipc

    # plot data
    if multicore == 1:
        plot_data_multicore(lru_map_lis, ship_map_lis, myrepl_map_lis, tracelis)
    else:
        plot_data(lru_map, ship_map, myrepl_map)

