# %%
# # data science notebook 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# load point_df, curve_df, and density_df .csv files from csvExports folder
point_df = pd.read_csv('csvExports/point_df.csv')
curve_df = pd.read_csv('csvExports/curve_df.csv')
density_df = pd.read_csv('csvExports/density_df.csv')
print ('Data Loaded')
point_df

# %%%
#####










# %%
#####  ####### PCA investigation... probably not the route i wanted to go
#############
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import pandas as pd

# Assuming point_df is your DataFrame and it's already loaded

# Step 1: Standardize the data
# Select numerical features for standardization and PCA
numerical_features = point_df.select_dtypes(include=['float64', 'int64']).columns.tolist()
# Remove 'roastCount' if it's not intended to be part of the clustering features
numerical_features.remove('roastCount')
#remove other columns that are not needed for clustering
# Assuming numerical_features is a list of column names from point_df
desired_columns = ['drumChargeTemperature', 'drumDropTemperature', 'preheatTemperature', 'weightGreen', 'weightRoasted', 'weightLostPercent',
                   'totalRoastTime', 'indexFirstCrackStart', 'firstCrackTime', 'ibtsTurningPointTemp', 'firstCrackTemp', 'turningPointTime', 
                   'yellowPointTime', 'peakROR', 'deltaIBTS-BT-atDrop', 'yellowingPhaseTime', 'browningPhaseTime', 'developmentTime', 
                   'RoR-yellowing-est', 'RoR-browning-est', 'RoR-development-est', 'RoR-fullRoast-est']
# Filter numerical_features to only include the desired columns
numerical_features = [column for column in numerical_features if column in desired_columns]
# drop rows with NaN values in numerical_features
point_df = point_df.dropna(subset=numerical_features)

print (numerical_features)


# %%
data = point_df[numerical_features]
# Standardize the features
scaler = StandardScaler()
scaled_features = scaler.fit_transform(data)

#%%
#####  TECHNIQUE for reviewing variance in the PCA components

# Explained variance ratio
explained_variance_ratio = pca.explained_variance_ratio_
print("Explained Variance Ratio by Principal Component:")
print(explained_variance_ratio)
import matplotlib.pyplot as plt

explained_variance_ratio = [0.35116075, 0.18172623, 0.12112452, 0.10129286, 0.08498498, 0.04229619, 0.03463761]

cumulative_variance = np.cumsum(explained_variance_ratio)
print("Cumulative Explained Variance:")
print(cumulative_variance)

# Plot explained variance ratio
plt.figure(figsize=(10, 5))
plt.bar(range(1, len(explained_variance_ratio) + 1), explained_variance_ratio, alpha=0.5, align='center', label='individual explained variance')
plt.step(range(1, len(explained_variance_ratio) + 1), cumulative_variance, where='mid', label='cumulative explained variance')
plt.ylabel('Explained variance ratio')
plt.xlabel('Principal components')
plt.title('Explained Variance Ratio by Principal Component')
plt.legend(loc='best')
plt.show()

# %%
# Loadings (coefficients)
loadings = pca.components_.T
loadings_df = pd.DataFrame(loadings, index=data.columns, columns=[f'PC{i+1}' for i in range(loadings.shape[1])])
print("\nLoadings (Principal Component Coefficients):")
print(loadings_df)


#####
### From these loadings, I can see some duplicated columns (like indexFirstCrackStart and firstCrackTime) that I can remove from the clustering features.
### I can see from the PCA - groups of relatively related features such as
## PC1: Roast and phase Timing: firstCrackTime, totalRoastTime, developmentTime, yellowPointTime, RoR-yellowing-est, browningPhaseTime, 
## PC2: Roast prep and early roast features: preheatTemperature, weightRoasted, weightGreen, deltaIBTS-BT-atDrop, drumDropTemperature, turningPointTime, peakROR
## PC3: Charge, drop, and weight (?): drumChargeTemperature, drumDropTemperature, RoR-fullRoast-est, weightRoasted, weightGreen, firstCrackTemp
## pC4: less clear simliar to PC3 ?: ibtsTurningPointTemp, RoR-development-est, turningPointTime, weightLostPercent, yellowingPhaseTime 

####
# %% 
# Step 2: Apply PCA
pca = PCA(n_components=0.90)  # Adjust n_components to retain 90% of variance
pca_features = pca.fit_transform(scaled_features)

# Step 3: Apply KMeans Clustering
# Initialize the KMeans model with 4 clusters determined by the elbow plot
kmeans = KMeans(n_clusters=4, random_state=42)
point_df['cluster'] = kmeans.fit_predict(pca_features)

# Optional: Export the DataFrame with cluster labels
#point_df.to_csv('csvExports/point_df_with_clusters.csv', index=False)
# create a new plot using mat plot lib to visuallize the clusters by plotting the PCA features
# plot the clusters
import matplotlib.pyplot as plt
plt.scatter(pca_features[:, 0], pca_features[:, 1], c=point_df['cluster'], cmap='viridis')
plt.xlabel('PCA Feature 1')
plt.ylabel('PCA Feature 2')
plt.title('KMeans Clustering of Coffee Roasting Data')
plt.show()



print("PCA and KMeans Clustering Complete")

# %%
# use an elbow plot to determine the optimal number of clusters
# Create a list to store the inertia values
inertia = []

# Create a range of K values to test
k_values = range(1, 11)

# Iterate over the range of K values
for k in k_values:
    # Initialize the KMeans model with the current K value
    kmeans = KMeans(n_clusters=k, random_state=42)
    
    # Fit the model to the PCA features
    kmeans.fit(pca_features)
    
    # Append the inertia value to the list
    inertia.append(kmeans.inertia_)
    
# Plot the inertia values against K values
plt.figure(figsize=(10, 6))
plt.plot(k_values, inertia, marker='o')
plt.xlabel('Number of Clusters (K)')
plt.ylabel('Inertia')
plt.title('Elbow Plot of KMeans Clustering')
plt.show()



# %% 
# # Simple QC Plots #
# plot_bar(point_df)
# plot_box(point_df)
plot_scatter(point_df)

# %%
##################################

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
####################





# quick review with a correlation matrix
import seaborn as sns
#from src.GsheetDensity import getDensityGSheetPublic ***
import matplotlib.pyplot as plt

# Load your data

# Select only numeric columns
numeric_df = point_df.select_dtypes(include=[float, int])
numeric_df = numeric_df.drop(columns=['indexFirstCrackStart', 'indexTurningPoint', 'index165PT', 'dateTime', 'firmware', 'roastCount', 'yellowPointTemp165'], errors='ignore')

# Calculate the correlation matrix
corr_matrix = numeric_df.corr()

# Adjust figure size for better readability
plt.figure(figsize=(16, 12))  # Increase the size of the figure

# Create a heatmap with rotated labels and smaller annotations
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", annot_kws={"size": 8})

# Rotate x and y labels
plt.xticks(rotation=45, ha='right')  # Rotate x labels
plt.yticks(rotation=0)  # Keep y labels horizontal

plt.title('Correlation Matrix of Coffee Roasting Data')
#save the plot to a image file to the images folder
plt.savefig('images/CorrelationMatrix.png')
plt.show()



# %% 
# Show a pairplot of numeric_df
sns.pairplot(numeric_df)
#save the plot to a image file to the images folder
plt.savefig('images/PairPlot.png')
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
#save the plot to a image file to the images folder
plt.savefig('images/IBTS_Derivative_Values.png')
plt.show()
# %%
