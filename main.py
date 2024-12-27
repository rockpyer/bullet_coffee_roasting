#%%
"""
This script performs coffee roasting data analysis and visualization for RoasTime data from the Allio Bullet.
It has code cell markers to help naviate and run the code in VS Code or Jupyter Notebook extensions.
1. Load roasting data from a specified directory.
2. Perform basic data cleanup.
3. Deconstruct temperature curves from lists to a new curve DataFrame & create a point DataFrame.
4. Fill NaN values.
5. Develop the point DataFrame by adding derived attributes.
6. Use an AI model to extract the origin of the coffee beans.
7. Export the processed curve DataFrame and point DataFrame to CSV files.
8. Clean up, check and visualize some data.
"""
import logging
import os
import numpy as np
import pandas as pd
from src.data_load import load_roasting_data
from src.data_cleanup import basic_cleanup, fill_derivative_values, drop_intermediate_columns
from src.data_processing import deconstruct_temp_curves, develop_point_df, check_missing_values, create_point_df, calculate_roast_milestone_points
from src.data_export import export_raw_data, export_processed_data
from src.plots import plot_scatter#, plot_bar, plot_box, plot_scatter_matrix
from dotenv import load_dotenv

logging.basicConfig(filename='log_file.log', level=logging.DEBUG)

# Set Max columns to 100
pd.set_option('display.max_columns', 100)
# set up the data frame to be more readable
pd.set_option('display.width', 1000)

# Load from roasTime repository on macOS
home = os.path.expanduser('~')
base_path = os.path.join(home, 'Library/Application Support/roast-time/roasts')
##  IF you have a specific set of roast profiles in another folder, uncomment and adjust the line below
# base_path = Path('/data')

# Load the roasting data
df = load_roasting_data(base_path)

# Perform basic data cleanup
df = basic_cleanup(df)
print ("Basic Cleanup Complete")

# Export the raw DataFrame to a .csv file
export_raw_data(df)
print ("Export Raw Data Complete")
#display (df)

curve_df = deconstruct_temp_curves(df)
print ("Deconstruct Complete")

# create point_df
point_df = create_point_df(df)
print ("Create Point_df Complete")

curve_df = fill_derivative_values(curve_df)
print ('Filled nan values in derivative (starting values have no derivative)')

# get first crack temp
point_df = calculate_roast_milestone_points(curve_df, point_df)
print ("Calculate_roast_milestone_points Complete")

# drop   'indexFirstCrackStart' column from curve_df
curve_df = curve_df.drop(columns=['indexFirstCrackStart']) # *** future move this to a clean up function

# Develop Point_DF
point_df = develop_point_df(point_df, curve_df)
print ("Develop point_df Complete, point_df so far:")

print ("n/")
display (point_df)




# %%
################ ################## ############### #############
### OPENAI API call to get ORIGIN and ROAST COUNT from the roastName in an async call
## You would have to set up system variables for the OPENAI_API_KEY
## This is a workflow for my methods, may not be generally useful, comment out if not needed.
import nest_asyncio
import asyncio
from src.AI import process_roast_names

# Apply nest_asyncio
nest_asyncio.apply()

AI_model = "gpt-4o-mini"
roast_names = point_df['roastName'].tolist()  # Get a list of roast names from the DataFrame

# Call the async function
results = asyncio.run(process_roast_names(roast_names, AI_model))


# Convert the results to a DataFrame
results_df = pd.DataFrame(results, columns=['Origin', 'roastCount'])
results_df['roastName'] = roast_names  # Add the roast names to the results DataFrame

# Merge the results back into the original DataFrame
point_df = point_df.merge(results_df, on='roastName', how='left')
point_df

# %%
############## ################ ################## ##############
############ Density from Google Sheets workflow  ####################################
############ This is a private workflow, that may not be useful to others ############
# private .env file is not included in the repository, has all the info about my gsheet

from src.GsheetDensity import getDensityGSheetPublic
# Call the getDensityGSheet function to retrieve the density data from Google Sheets


#density_df = getDensityGSheet()
density_df = getDensityGSheetPublic()


## Planned to do:
## 1. Merge density_df with point_df
## 2. do some light analysis on density related to roastTime/Temp
## 3. review soak to TP relationships
## 4. consider if I can create a sliding variable of 'early roast power' to better define soak and the relationship to TP
## 5. lots more denisty stuff
## 6. move this or the analysis to another .py file.  this one being the data processing and export


# Print the density_df to verify the data
print(density_df)

# %%
#######################################################################################
#########  FINISHING STEPS and RESULTS and EXPORT  ####################################
#######################################################################################
print (point_df)  # *** future pip install tabulate and print(tabulate(point_df, headers='keys', tablefmt='psql')) 
print (curve_df) ## removed notebook display methods so it works for others

#### FINAL CLEANUP and EXPORT #####
# Post-process cleanup
point_df = drop_intermediate_columns(point_df)
print ("Post-process cleanup Complete")

# Check
check_missing_values(point_df)

# Export the processed curve_df and point_df to a .csv file
#######
export_processed_data(curve_df, point_df)
# export density_df to csv in subfolder = 'csvExports/'  *** future add to above function
# *** add a timestamp or better yet, consider a system to not clutter the folder with multiple exports
density_df.to_csv('csvExports/density_df.csv', index=False)

print ("Export point_df, curve_df, and density_df to csv Complete")
print ("All Done!")

 # %%
 # ######## WORKING ###########    ########
 #############################    #####

 
################################################## =============== ###############

# Clean up and review of DensityGSheet,   bring in density data into point_df
# count unique roastCount values and rows in point_df
print(point_df['roastCount'].nunique())
display (point_df['roastCount'].value_counts())
print(point_df.shape[0])
#Merge density_df with point_df on roastCount 
point_df = pd.merge(point_df, density_df, on='roastCount', how='left')
#drop blank column, roasted gram & other density notes in point_df
point_df = point_df.drop(columns=['', 'roastedGram', 'densityNotes'], errors='ignore')
display (point_df)

# %%
