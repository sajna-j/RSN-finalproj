# RSN-finalproj

all data is available in pandas dataframes!

Any scripts you need to make should be added to the `scripts` folder and you can access the data by including this entire statement at the top of your file:
```
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
```

To access the columns of the dataframe, you can write something like `thigh_stairs_test_df['magX']` to see the entire column of magnetometer X readings. 
To best work with the columns, convert them to numpy arrays like so: `thigh_stairs_test_df['magX'].to_numpy()`
To view the column labels: `print(thigh_stairs_test_df)` or another df to see all the titles
