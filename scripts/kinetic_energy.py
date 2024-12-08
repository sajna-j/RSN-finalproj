import numpy as np
import pandas as pd
from scipy.spatial.transform import Rotation as R
from scipy.integrate import cumulative_trapezoid
import matplotlib.pyplot as plt
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


# Function to remove gravity from IMU acceleration
def remove_gravity(df):
    g_world = np.array([0, 0, 9.81])  # Gravity vector in world frame
    acc_linear = []
    
    for i in range(len(df)):
        quat = df.loc[i, ['orientationX', 'orientationY', 'orientationZ', 'orientationW']].values
        r = R.from_quat(quat)
        g_imu = r.apply(g_world)
        acc_raw = df.loc[i, ['linear_accX', 'linear_accY', 'linear_accZ']].values
        acc_linear.append(acc_raw - g_imu)
    
    acc_linear = np.array(acc_linear)
    df['accX_corrected'] = acc_linear[:, 0]
    df['accY_corrected'] = acc_linear[:, 1]
    df['accZ_corrected'] = acc_linear[:, 2]
    return df

# Function to integrate acceleration and compute kinetic energy
def calculate_kinetic_energy(df, segment_mass):
    time = df['time'].values
    acc = df[['accX_corrected', 'accY_corrected', 'accZ_corrected']].values

    velocity = cumulative_trapezoid(acc, time, initial=0, axis=0)
    speed = np.linalg.norm(velocity, axis=1)
    KE = 0.5 * segment_mass * (speed ** 2)
    return time, KE

# Plot multiple datasets on the same subplot
def plot_comparative_kinetic_energy(datasets, titles, segment_mass, main_title, location):
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    stairs_ax, ramp_ax = axes
    
    # Plot stairs datasets
    stairs_ax.set_title(f'{location} Stairs')
    for df, title in datasets['stairs']:
        df = remove_gravity(df)
        time, KE = calculate_kinetic_energy(df, segment_mass[title])
        stairs_ax.plot(time, KE, label=title)
    
    stairs_ax.set_xlabel('Time (s)')
    stairs_ax.set_ylabel('Kinetic Energy (Joules)')
    stairs_ax.legend()
    stairs_ax.grid()

    # Plot ramp datasets
    ramp_ax.set_title(f'{location} Ramps')
    for df, title in datasets['ramps']:
        df = remove_gravity(df)
        time, KE = calculate_kinetic_energy(df, segment_mass[title])
        ramp_ax.plot(time, KE, label=title)
    
    ramp_ax.set_xlabel('Time (s)')
    ramp_ax.legend()
    ramp_ax.grid()

    plt.suptitle(main_title)
    plt.tight_layout()
    plt.show()

# Define datasets and masses
body_mass = 70
segment_mass = {'thigh': 0.10 * body_mass, 'calf': 0.045 * body_mass}

datasets_carter = {
    'stairs': [
        (calf_carter_stairs1_df, 'Carter Stairs 1 Calf'),
        (calf_carter_stairs2_df, 'Carter Stairs 2 Calf'),
        (thigh_carter_stairs1_df, 'Carter Stairs 1 Thigh'),
        (thigh_carter_stairs2_df, 'Carter Stairs 2 Thigh'),
    ],
    'ramps': [
        (calf_carter_ramp1_df, 'Carter Ramp 1 Calf'),
        (calf_carter_ramp2_df, 'Carter Ramp 2 Calf'),
        (thigh_carter_ramp1_df, 'Carter Ramp 1 Thigh'),
        (thigh_carter_ramp2_df, 'Carter Ramp 2 Thigh'),
    ],
}

datasets_law = {
    'stairs': [
        (calf_law_stairs1_df, 'Law Stairs 1 Calf'),
        (calf_law_stairs2_df, 'Law Stairs 2 Calf'),
        (thigh_law_stairs1_df, 'Law Stairs 1 Thigh'),
        (thigh_law_stairs2_df, 'Law Stairs 2 Thigh'),
    ],
    'ramps': [
        (calf_law_ramp1_df, 'Law Ramp 1 Calf'),
        (calf_law_ramp2_df, 'Law Ramp 2 Calf'),
        (thigh_law_ramp1_df, 'Law Ramp 1 Thigh'),
        (thigh_law_ramp2_df, 'Law Ramp 2 Thigh'),
    ],
}

# Plot for Carter
plot_comparative_kinetic_energy(datasets_carter, titles=['Stairs', 'Ramps'],
                                segment_mass={'Carter Stairs 1 Calf': segment_mass['calf'],
                                              'Carter Stairs 2 Calf': segment_mass['calf'],
                                              'Carter Stairs 1 Thigh': segment_mass['thigh'],
                                              'Carter Stairs 2 Thigh': segment_mass['thigh'],
                                              'Carter Ramp 1 Calf': segment_mass['calf'],
                                              'Carter Ramp 2 Calf': segment_mass['calf'],
                                              'Carter Ramp 1 Thigh': segment_mass['thigh'],
                                              'Carter Ramp 2 Thigh': segment_mass['thigh']},
                                main_title='Carter Stairs vs Ramps Kinetic Energy',
                                location="Carter")

# Plot for Law
plot_comparative_kinetic_energy(datasets_law, titles=['Stairs', 'Ramps'],
                                segment_mass={'Law Stairs 1 Calf': segment_mass['calf'],
                                              'Law Stairs 2 Calf': segment_mass['calf'],
                                              'Law Stairs 1 Thigh': segment_mass['thigh'],
                                              'Law Stairs 2 Thigh': segment_mass['thigh'],
                                              'Law Ramp 1 Calf': segment_mass['calf'],
                                              'Law Ramp 2 Calf': segment_mass['calf'],
                                              'Law Ramp 1 Thigh': segment_mass['thigh'],
                                              'Law Ramp 2 Thigh': segment_mass['thigh']},
                                main_title='Law Stairs vs Ramps Kinetic Energy',
                                location="Law School")
