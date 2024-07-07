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

        print (f'Exported {point_filename} and {curve_filename} to csvExports folder')

        # Convert point_df to JSON format
        point_JSONfilename = f'point_data_{timestamp}.json'
        point_df_json = point_df.to_json(orient='records')
        # Export the JSON data to a file
        with open(subfolder + point_JSONfilename, 'w') as file:
            file.write(point_df_json)

        print("Exported point_df to JSON Done")
    except Exception as e:
        debug_info = f"An error occurred: {e}"

        print(f"An error occurred: {e}")
