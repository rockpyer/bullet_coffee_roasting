import os

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
    # Create subfolder if it doesn't exist
    subfolder = 'csvExports/'
    if not os.path.exists(subfolder):
        os.makedirs(subfolder)

    # Export the raw DataFrame to a .csv file
    curve_df.to_csv(subfolder + "curve_df.csv", index=False)
    point_df.to_csv(subfolder + "point_df.csv", index=False)
    
    