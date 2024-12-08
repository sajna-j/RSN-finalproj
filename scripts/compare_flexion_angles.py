from typing import List
from scipy.signal import butter, sosfilt, freqz
from bag_dataframes import (
    # CALF DATASETS
    calf_law_stairs1_df, calf_law_stairs2_df,
    calf_law_ramp1_df, calf_law_ramp2_df, calf_law_incline_df, calf_law_decline_df,
    calf_carter_stairs1_df, calf_carter_stairs2_df,
    calf_carter_ramp1_df, calf_carter_ramp2_df, calf_carter_incline_df, calf_carter_decline_df,
    calf_stairs_test_df, calf_sitting_test_df, calf_standing_test_df, calf_walking_test_df,

    # THIGH DATASETS
    thigh_law_stairs1_df, thigh_law_stairs2_df,
    thigh_law_ramp1_df, thigh_law_ramp2_df, thigh_law_incline_df, thigh_law_decline_df,
    thigh_carter_stairs1_df, thigh_carter_stairs2_df,
    thigh_carter_ramp1_df, thigh_carter_ramp2_df, thigh_carter_incline_df, thigh_carter_decline_df,
    thigh_stairs_test_df, thigh_sitting_test_df, thigh_walking_test_df, thigh_standing_test_df
)

import matplotlib.pyplot as plt
sampl_freq=40
cutoff_freq=3
order=4

def butter_filter(raw_data, cutoff_freq, sampl_freq, filt_type, filt_order):
    nyq_freq = sampl_freq / 2 #set the Nyquist frequency (important to avoid aliasing)
    sos = butter(N = filt_order, Wn = cutoff_freq / nyq_freq, btype=filt_type, analog=False, output='sos')
    filtered_data = sosfilt(sos, raw_data)
    return sos, filtered_data

def plot_scatter(df, title, xlabel, ylabel, scatters: List[str], x_column='time'):
    """
    Create a scatter plot with multiple datasets.

    Parameters:
    - title (str): Title of the plot.
    - xlabel (str): Label for the X-axis.
    - ylabel (str): Label for the Y-axis.
    - scatter_datasets (list of dict): Each dataset is a dictionary with:
        - 'x' (list or array): X values.
        - 'y' (list or array): Y values.
        - 'label' (str): Label for the dataset (optional).
        - 'color' (str, optional): Color for the scatter points.
        - 'marker' (str, optional): Marker style for scatter points.

    Example Usage:
    plot_scatter(
        title="Example Scatter Plot",
        xlabel="X-axis Label",
        ylabel="Y-axis Label",
        scatter_datasets=[
            {'x': [1, 2, 3], 'y': [4, 5, 6], 'label': 'Dataset 1', 'color': 'red', 'marker': 'o'},
            {'x': [2, 3, 4], 'y': [3, 4, 5], 'label': 'Dataset 2', 'color': 'blue', 'marker': 'x'}
        ]
    )
    """
    plt.figure(figsize=(12, 7))

    # Loop through each scatter dataset and plot
    x = df[x_column].to_numpy()
    for data_label in scatters:
        y = df[data_label].to_numpy()
        plt.plot(x, y, label=data_label, linestyle='-')

        # I'm filtering the dataset to make room for us to be able to get like CLEAR mins/maxes 
        #   and compare the typical angle upwards for each body part and compare (hopefully higher for thigh, but seems to be otherwise)
        # sample freq. is 40, I set the cutoff to 3 Hz bc we def don't walk fast enough to make 3 steps a sec
        sos, filtered_y = butter_filter(y, cutoff_freq, sampl_freq, "lowpass", 5)
        plt.plot(x, filtered_y, label=f"{data_label} filtered", linestyle='-')

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid()
    plt.title(title)
    plt.grid(True)
    plt.show()


def calibrate(df, columns, start_sec=3, end_sec=8):
    """
    remove the standing calibration value we calculated (assumed to be standing btwn 3-8 s)
    This will remove the initial offset of our values to start them closer to 0.

    Parameters:
    - df (pd.DataFrame): DataFrame containing the data.
    - time_col (str): Name of the time column in nanoseconds.
    - columns (str): Name of the magZ column.
    - start_sec (int): Start time in seconds.
    - end_sec (int): End time in seconds.
    """

    # Step 2: Filter rows where time is between start_sec and end_sec
    filtered_df = df[(df['time'] >= start_sec) & (df['time'] <= end_sec)]
    
    # Step 3: get the mean for that time section of column
    for column in columns:
        calibration_mean_column = filtered_df[column].mean()
        df[column] = df[column] - calibration_mean_column


"""
plot_scatter(thigh_law_stairs1_df, "Magnetometer", "Reading (rad)", "Time (s)", ["magX","magY","magZ"])
calibrate(thigh_law_stairs1_df, ["magX","magY","magZ"])
plot_scatter(thigh_law_stairs1_df, "Magnetometer", "Reading (rad)", "Time (s)", ["magX","magY","magZ"])
"""

calibrate(thigh_carter_stairs1_df, ["magZ"])
plot_scatter(thigh_carter_stairs1_df, "Magnetometer Thigh Stairs Carter 1", "Time (s)", "Reading (rad)", ["magZ"])

calibrate(thigh_carter_stairs2_df, ['magZ'])
plot_scatter(thigh_carter_stairs2_df, "Magnetometer Thigh Stairs Carter 2", "Time (s)", "Reading (rad)", ["magZ"])

calibrate(thigh_carter_ramp1_df, ["magZ"])
plot_scatter(thigh_carter_ramp1_df, "Magnetometer Thigh Ramp Carter 1", "Time (s)", "Reading (rad)", ["magZ"])

calibrate(thigh_carter_ramp2_df, ["magZ"])
plot_scatter(thigh_carter_ramp2_df, "Magnetometer Thigh Ramp Carter 2", "Time (s)", "Reading (rad)", ["magZ"])

# TODO: do the above for all of the stairs and ramps datasets

# TODO: find a way to remove the angle from the inclines? but these removals are specific to sections of walking up/down
# TODO: make a statement about thigh angle in the ramp vs stairs 
    # seemingly, the ramp shows a higher angle for the thigh flexion? not what i assumed

# ROUTE 2:
# TODO: try integrating angular velocity around the Z to compare the total angles traveled for each dataset 
    # make sure to compare btwn each 1 and 2 of the datasets too before stairs vs ramp
# perhaps higher angles total traveled indicates more work put in?

# ROUTE 3:
# TODO: 1. calibrate the linear acceleration & estimate velocity through integration (like in lab5)
# 2. estimate kinetic energy at the thigh and calf with KE = 0.5*m*v^2
# 3. use approx. body segment mass: Thigh: 10% bodyweight, Calf: 5% body weight

# ROUTE 4:
# TODO: try converting this to dual point IMU analysis by getting knee flexion
# calibrate both datasets by subtracting their initial position (like the calibrate function above does)
# then, like in the readings, Roll_knee_flexion = Roll_thigh - Roll_calf
# try all of the above again and see if we can compare this dual point analysis with the claims made from the 
# single point analysis of how the calf did across the datasets
