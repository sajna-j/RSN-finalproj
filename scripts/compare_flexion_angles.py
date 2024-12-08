from typing import List
from scipy.signal import butter, sosfilt, freqz, savgol_filter, integrate
import numpy as np
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
cutoff_freq=1
order=4

def butter_filter(raw_data, cutoff_freq, sampl_freq, filt_type, filt_order):
    nyq_freq = sampl_freq / 2 #set the Nyquist frequency (important to avoid aliasing)
    sos = butter(N = filt_order, Wn = cutoff_freq / nyq_freq, btype=filt_type, analog=False, output='sos')
    filtered_data = sosfilt(sos, raw_data)
    return sos, filtered_data

def plot_scatter(df, title, xlabel, ylabel, scatters: list, x_column='time', cutoff_freq=3, sampl_freq=40):
    """
    Create a scatter plot with multiple datasets and display filtered data and its derivative.

    Parameters:
    - df (pd.DataFrame): The dataset.
    - title (str): Title of the scatter plot.
    - xlabel (str): Label for the X-axis.
    - ylabel (str): Label for the Y-axis.
    - scatters (list): List of column names to plot.
    - x_column (str): Column name for the X-axis data.
    - cutoff_freq (float): Cutoff frequency for filtering.
    - sampl_freq (float): Sampling frequency.
    """
    # Create subplots: 2 rows, 1 column
    fig, axs = plt.subplots(2, 1, figsize=(10, 8))
    x = df[x_column].to_numpy()

    # Subplot 1: Scatter and filtered data
    for data_label in scatters:
        y = df[data_label].to_numpy()

        # Plot raw data
        axs[0].plot(x, y, label=f"{data_label}", linestyle='-')

        # Apply low-pass filter
        sos, filtered_y = butter_filter(y, cutoff_freq, sampl_freq, "lowpass", 5)
        axs[0].plot(x, filtered_y, label=f"{data_label} filtered", linestyle='--')

        # Calculate derivative
        smooth_deriv = savgol_filter(filtered_y, window_length=5, polyorder=2, deriv=1, delta=1)

        # Calculate positive and negative derivative averages
        positive_derivs = smooth_deriv[smooth_deriv > 0]  # Filter positive values to represent EXTENSION
        negative_derivs = smooth_deriv[smooth_deriv < 0]  # Filter negative values to represent FLEXION
        avg_pos_deriv = np.mean(positive_derivs) if len(positive_derivs) > 0 else 0
        avg_neg_deriv = np.mean(negative_derivs) if len(negative_derivs) > 0 else 0
        print(title)
        print(round(avg_pos_deriv, 5), " = AVG Flexion Derivative")
        print(round(avg_neg_deriv, 5), " = AVG Extension Derivative")
        print(f"Ext {'<' if avg_pos_deriv < abs(avg_neg_deriv) else '>'} Flex")
        print()

    # Formatting for Subplot 1
    axs[0].set_title(title)
    axs[0].set_xlabel(xlabel)
    axs[0].set_ylabel(ylabel)
    axs[0].legend()
    axs[0].grid()

    # Subplot 2: Derivative of filtered data
    axs[1].plot(x, smooth_deriv, label='Derivative', linestyle='-')
    axs[1].set_title("Derivative of Filtered Data")
    axs[1].set_xlabel("Time")
    axs[1].set_ylabel("Derivative Value")
    axs[1].legend()
    axs[1].grid()

    # Adjust layout and show the figure
    plt.tight_layout()
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

calibrate(calf_carter_stairs1_df, ["magZ"])
plot_scatter(calf_carter_stairs1_df, "Magnetometer Calf Stairs Carter 1", "Time (s)", "Reading (rad)", ["magZ"])

calibrate(calf_carter_stairs2_df, ['magZ'])
plot_scatter(calf_carter_stairs2_df, "Magnetometer Calf Stairs Carter 2", "Time (s)", "Reading (rad)", ["magZ"])

calibrate(calf_carter_ramp1_df, ["magZ"])
plot_scatter(calf_carter_ramp1_df, "Magnetometer Calf Ramp Carter 1", "Time (s)", "Reading (rad)", ["magZ"])

calibrate(calf_carter_ramp2_df, ["magZ"])
plot_scatter(calf_carter_ramp2_df, "Magnetometer Calf Ramp Carter 2", "Time (s)", "Reading (rad)", ["magZ"])

calibrate(thigh_law_stairs1_df, ["magZ"])
plot_scatter(thigh_law_stairs1_df, "Magnetometer Thigh Stairs Law 1", "Time (s)", "Reading (rad)", ["magZ"])

calibrate(thigh_law_stairs2_df, ['magZ'])
plot_scatter(thigh_law_stairs2_df, "Magnetometer Thigh Stairs Law 2", "Time (s)", "Reading (rad)", ["magZ"])

calibrate(thigh_law_ramp1_df, ["magZ"])
plot_scatter(thigh_law_ramp1_df, "Magnetometer Thigh Ramp Law 1", "Time (s)", "Reading (rad)", ["magZ"])

calibrate(thigh_law_ramp2_df, ["magZ"])
plot_scatter(thigh_law_ramp2_df, "Magnetometer Thigh Ramp Law 2", "Time (s)", "Reading (rad)", ["magZ"])

calibrate(calf_law_stairs1_df, ["magZ"])
plot_scatter(calf_law_stairs1_df, "Magnetometer Calf Stairs Law 1", "Time (s)", "Reading (rad)", ["magZ"])

calibrate(calf_law_stairs2_df, ['magZ'])
plot_scatter(calf_law_stairs2_df, "Magnetometer Calf Stairs Law 2", "Time (s)", "Reading (rad)", ["magZ"])

calibrate(calf_law_ramp1_df, ["magZ"])
plot_scatter(calf_law_ramp1_df, "Magnetometer Calf Ramp Law 1", "Time (s)", "Reading (rad)", ["magZ"])

calibrate(calf_law_ramp2_df, ["magZ"])
plot_scatter(calf_law_ramp2_df, "Magnetometer Calf Ramp Law 2", "Time (s)", "Reading (rad)", ["magZ"])




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
