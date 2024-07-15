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
import time
import numpy as np
import pandas as pd
#from importlib import reload
#from pathlib import Path
#from pprint import pprint
from src.data_load import load_roasting_data
from src.data_cleanup import basic_cleanup, fill_derivative_values, drop_intermediate_columns
from src.data_processing import deconstruct_temp_curves, develop_point_df, check_missing_values, create_point_df, get_first_crack_temp
from src.data_export import export_raw_data, export_processed_data
from src.plots import plot_scatter#, plot_bar, plot_box, plot_scatter_matrix
from src.plots import plot_scatter#, plot_bar, plot_box, plot_scatter_matrix
from src.AI import get_origin

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
print ('Filled nan values in derivative')

# get first crack temp
point_df = get_first_crack_temp(curve_df, point_df)
print ("Get First Crack Temp Complete")

# drop   'indexFirstCrackStart' column from curve_df
curve_df = curve_df.drop(columns=['indexFirstCrackStart']) # *** future move this to a clean up function

# Develop Point_DF
point_df = develop_point_df(point_df, curve_df)
print ("Develop Point_DF Complete")

# %%  
# seperate AI CALL for a min to not run it
####### Use OpenAI to get the origin from the roastName ########
from src.AI import get_origin
start_time = time.time()
print ("Geting Origin....standby")
point_df['Origin'] = point_df['roastName'].apply(get_origin)

end_time = time.time()
elapsed_time = end_time - start_time
print(f"Get Origin Complete. Function took {elapsed_time} seconds to run.")


# %% # View results 
######## RESULTS and EXPORT ########################################
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
print ("Export Processed Data to csv Complete")



 #%%
# Simple QC Plots #
# plot_bar(point_df)
# plot_box(point_df)
plot_scatter(point_df)

#plot_scatter_matrix(point_df) #currently has issuse with missing values
# In the dataframe passed, the following columns have missing values: 
# ['weightLostPercent', 'ambient', 'humidity', 'Drop-ChargeDeltaTemp', 
# 'comments', 'rating', 'beanId', 'indexTurningPoint', 'ibtsTurningPointTemp', 
# 'turningPointTime']



# %%
#view outliers
# Calculate the Z-score for each observation in the 'beanChargeTemperature' column
z_scores = np.abs((point_df['beanChargeTemperature'] - point_df['beanChargeTemperature'].mean()) / point_df['beanChargeTemperature'].std())

# Set a threshold for the Z-score to identify outliers in the 'beanChargeTemperature'
threshold = 3

# Filter the dataframe to only include observations with a Z-score greater than the threshold
outliers = point_df[z_scores > threshold]

# Print the outliers
print("outliners in beanChargeTemperature")
print(outliers[['roastName', 'beanChargeTemperature']])


# %%
# quick review with a correlation matrix
import seaborn as sns
import matplotlib.pyplot as plt

# Load your data

# Calculate correlation matrix
corr_matrix = point_df.corr()

# Plot heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
plt.title('Correlation Matrix of Coffee Roasting Data')
plt.show()

# %%
import matplotlib.pyplot as plt

# Step 1: Group curve_df by 'roastName'
grouped = curve_df.groupby('roastName')

# Step 2: Identify the third to last roast name
roast_names = grouped.groups.keys()
roast_name = sorted(roast_names)[29]

# Step 3: Filter curve_df for the identified roast name
filtered_df = curve_df[curve_df['roastName'] == roast_name]

# Step 4: Plot the IBTS Derivative Values
plt.figure(figsize=(10, 6))
plt.plot(filtered_df['indexTime'], filtered_df['ibts2ndDerivative'], label='ibts2ndDerivative')
plt.title(f'IBTS Derivative for {roast_name}')
plt.xlabel('indexTime')
plt.ylabel('IBTS 2nd Derivative')
plt.ylim(-1, 25)
plt.legend()
plt.show()
# %%
