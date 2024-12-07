"""
Import all datasets from this file using:

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

"""
import os
import pandas as pd

current_folder = os.path.dirname(os.path.abspath(__file__))
csvs_folder = os.path.abspath(os.path.join(current_folder, '..', 'csvs'))
thigh_folder = os.path.join(csvs_folder, 'thigh')
calf_folder = os.path.join(csvs_folder, 'calf')

calf_files = ['calf_law_ramp1_df.csv', 'calf_carter_ramp1_df.csv', 'calf_stairs_test_df.csv', 'calf_carter_incline_df.csv', 'calf_law_incline_df.csv', 'calf_law_decline_df.csv', 'calf_carter_ramp2_df.csv', 'calf_sitting_test_df.csv', 'calf_carter_decline_df.csv', 'calf_carter_stairs1_df.csv', 'calf_law_stairs1_df.csv', 'calf_standing_test_df.csv', 'calf_law_stairs2_df.csv', 'calf_law_ramp2_df.csv', 'calf_carter_stairs2_df.csv', 'calf_walking_test_df.csv']
thigh_files = ['thigh_carter_stairs1_df.csv', 'thigh_stairs_test_df.csv', 'thigh_sitting_test_df.csv', 'thigh_walking_test_df.csv', 'thigh_law_stairs1_df.csv', 'thigh_carter_decline_df.csv', 'thigh_law_ramp2_df.csv', 'thigh_law_decline_df.csv', 'thigh_law_stairs2_df.csv', 'thigh_law_incline_df.csv', 'thigh_carter_incline_df.csv', 'thigh_carter_ramp1_df.csv', 'thigh_standing_test_df.csv', 'thigh_carter_stairs2_df.csv', 'thigh_carter_ramp2_df.csv', 'thigh_law_ramp1_df.csv']

################### CALF DATASETS
calf_law_stairs1_df = pd.read_csv(os.path.join(calf_folder, "calf_law_stairs1_df.csv"))
calf_law_stairs2_df = pd.read_csv(os.path.join(calf_folder, "calf_law_stairs2_df.csv"))

calf_law_ramp1_df = pd.read_csv(os.path.join(calf_folder, "calf_law_ramp1_df.csv"))
calf_law_ramp2_df = pd.read_csv(os.path.join(calf_folder, "calf_law_ramp2_df.csv"))
calf_law_incline_df = pd.read_csv(os.path.join(calf_folder, "calf_law_incline_df.csv"))
calf_law_decline_df = pd.read_csv(os.path.join(calf_folder, "calf_law_decline_df.csv"))

calf_carter_stairs1_df = pd.read_csv(os.path.join(calf_folder, "calf_carter_stairs1_df.csv"))
calf_carter_stairs2_df = pd.read_csv(os.path.join(calf_folder, "calf_carter_stairs2_df.csv"))

calf_carter_ramp1_df = pd.read_csv(os.path.join(calf_folder, "calf_carter_ramp1_df.csv"))
calf_carter_ramp2_df = pd.read_csv(os.path.join(calf_folder, "calf_carter_ramp2_df.csv"))
calf_carter_incline_df = pd.read_csv(os.path.join(calf_folder, "calf_carter_incline_df.csv"))
calf_carter_decline_df = pd.read_csv(os.path.join(calf_folder, "calf_carter_decline_df.csv"))

calf_stairs_test_df = pd.read_csv(os.path.join(calf_folder, "calf_stairs_test_df.csv"))
calf_sitting_test_df = pd.read_csv(os.path.join(calf_folder, "calf_sitting_test_df.csv"))
calf_standing_test_df = pd.read_csv(os.path.join(calf_folder, "calf_standing_test_df.csv"))
calf_walking_test_df = pd.read_csv(os.path.join(calf_folder, "calf_walking_test_df.csv"))

################## THIGH DATASETS
thigh_law_stairs1_df = pd.read_csv(os.path.join(thigh_folder, "thigh_law_stairs1_df.csv"))
thigh_law_stairs2_df = pd.read_csv(os.path.join(thigh_folder, "thigh_law_stairs2_df.csv"))

thigh_law_ramp1_df = pd.read_csv(os.path.join(thigh_folder, "thigh_law_ramp1_df.csv"))
thigh_law_ramp2_df = pd.read_csv(os.path.join(thigh_folder, "thigh_law_ramp2_df.csv"))
thigh_law_incline_df = pd.read_csv(os.path.join(thigh_folder, "thigh_law_incline_df.csv"))
thigh_law_decline_df = pd.read_csv(os.path.join(thigh_folder, "thigh_law_decline_df.csv"))

thigh_carter_stairs1_df = pd.read_csv(os.path.join(thigh_folder, "thigh_carter_stairs1_df.csv"))
thigh_carter_stairs2_df = pd.read_csv(os.path.join(thigh_folder, "thigh_carter_stairs2_df.csv"))

thigh_carter_ramp1_df = pd.read_csv(os.path.join(thigh_folder, "thigh_carter_ramp1_df.csv"))
thigh_carter_ramp2_df = pd.read_csv(os.path.join(thigh_folder, "thigh_carter_ramp2_df.csv"))
thigh_carter_incline_df = pd.read_csv(os.path.join(thigh_folder, "thigh_carter_incline_df.csv"))
thigh_carter_decline_df = pd.read_csv(os.path.join(thigh_folder, "thigh_carter_decline_df.csv"))

thigh_stairs_test_df = pd.read_csv(os.path.join(thigh_folder, "thigh_stairs_test_df.csv"))
thigh_sitting_test_df = pd.read_csv(os.path.join(thigh_folder, "thigh_sitting_test_df.csv"))
thigh_walking_test_df = pd.read_csv(os.path.join(thigh_folder, "thigh_walking_test_df.csv"))
thigh_standing_test_df = pd.read_csv(os.path.join(thigh_folder, "thigh_standing_test_df.csv"))
