import os
import rosbag
import pandas as pd

print(os.getcwd())

# Get the absolute path of the script's current directory
current_folder = os.path.dirname(os.path.abspath(__file__))
bags_folder = os.path.join(current_folder, '..', 'bags')
bags_folder = os.path.abspath(bags_folder)
csvs_folder = os.path.abspath(os.path.join(current_folder, '..', 'csvs'))
thigh_folder = os.path.join(csvs_folder, 'thigh')
calf_folder = os.path.join(csvs_folder, 'calf')
print("Bags folder path:", bags_folder)

file_paths = [os.path.join(bags_folder, file) for file in os.listdir(bags_folder) if os.path.isfile(os.path.join(bags_folder, file))]
bag_files = os.listdir(bags_folder)

# Print file paths
for bag_file in bag_files:
    test_bag = rosbag.Bag(os.path.join(bags_folder, bag_file))
    thigh_topic = '/thigh'
    calf_topic = '/calf'
    bagname = bag_file[:-4]

    def get_dataframe(bag):
        thigh_data = []
        calf_data = []
        for topic, msg, t in bag.read_messages(topics=[thigh_topic, calf_topic]):
            time = t.to_sec()
            if topic == thigh_topic:
                thigh_data.append([time, msg.magnetic_field.x, msg.magnetic_field.y, msg.magnetic_field.z, 
                    msg.linear_acceleration.x, msg.linear_acceleration.y, msg.linear_acceleration.z, 
                    msg.angular_velocity.x, msg.angular_velocity.y, msg.angular_velocity.z, 
                    msg.orientation.x, msg.orientation.y, msg.orientation.z, msg.orientation.w])
            if topic == calf_topic:
                calf_data.append([time, msg.magnetic_field.x, msg.magnetic_field.y, msg.magnetic_field.z, 
                    msg.linear_acceleration.x, msg.linear_acceleration.y, msg.linear_acceleration.z, 
                    msg.angular_velocity.x, msg.angular_velocity.y, msg.angular_velocity.z, 
                    msg.orientation.x, msg.orientation.y, msg.orientation.z, msg.orientation.w])

        calf_df = pd.DataFrame(calf_data, columns=['time', 'magX', 'magY', 'magZ', 
            'linear_accX', 'linear_accY', 'linear_accZ', 
            "angular_velX", "angular_velY", "angular_velZ", 
            "orientationX", "orientationY", "orientationZ", "orientationW"])
        thigh_df = pd.DataFrame(thigh_data, columns=['time', 'magX', 'magY', 'magZ', 
            'linear_accX', 'linear_accY', 'linear_accZ', 
            "angular_velX", "angular_velY", "angular_velZ", 
            "orientationX", "orientationY", "orientationZ", "orientationW"])
        bag.close()
        return calf_df, thigh_df

    def remove_time_offset(df):
        df['time'] = df['time'] - df['time'][0]

    calf_df, thigh_df = get_dataframe(test_bag)

    for df in [thigh_df, calf_df]:
        remove_time_offset(df)

    thigh_df.to_csv(os.path.join(thigh_folder, f"thigh_{bagname}_df.csv"))
    calf_df.to_csv(os.path.join(calf_folder, f"calf_{bagname}_df.csv"))



