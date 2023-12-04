import os
from datetime import datetime

# export_raw_data(df)
def export_raw_data(df):
    # Create subfolder if it doesn't exist
    subfolder = 'csvExports/'
    if not os.path.exists(subfolder):
        os.makedirs(subfolder)

    # Export the raw DataFrame to a .csv file
    df.to_csv(subfolder + "raw_bullet-roasting_df.csv", index=False)
 
 
 
#export processed data curve_df and point_df
def export_processed_data(curve_df, point_df):
    try:
        # Create subfolder if it doesn't exist
        subfolder = 'csvExports/'
        if not os.path.exists(subfolder):
            os.makedirs(subfolder)

        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        point_filename = f'point_data_{timestamp}.csv'
        curve_filename = f'curve_data_{timestamp}.csv'

        # Export the raw DataFrame to a .csv file
        curve_df.to_csv(subfolder + curve_filename, index=False)
        point_df.to_csv(subfolder + point_filename, index=False)
        
        print ()
        print (f'Exported {point_filename} and {curve_filename} to csvExports folder')
    except Exception as e:
        print(f"An error occurred: {e}")