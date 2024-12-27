#this is creating two new df from the big old original df 
### curver_df as the individual temperature curves that are in a list and converting them to a dataframe
### point_df as single point attributes that are in a list and converting them to a dataframe
import pandas as pd
import numpy as np

# def deconstruct_temp_curves(df):
#     try:
#         temp_curve_df = pd.DataFrame()
#         curve_df = pd.DataFrame()
#         for index, row in df.iterrows():
#             temp_curve_df = pd.DataFrame([pd.Series(row['beanTemperature'], name='beanTemperature', dtype='float64'),
#                                         pd.Series(row['drumTemperature'], name='drumTemperature', dtype='float64'),
#                                         pd.Series(row['beanDerivative'], name='beanDerivative', dtype='float64'),
#                                         pd.Series(row['ibtsDerivative'], name='ibtsDerivative', dtype='float64')]).T
#             temp_curve_df['roastName'] = row['roastName']
#             temp_curve_df['indexTime'] = temp_curve_df.index
#             temp_curve_df['indexFirstCrackStart'] = row['indexFirstCrackStart']
#             temp_curve_df['softwareVersion'] = row['softwareVersion']
#             curve_df = pd.concat([curve_df, temp_curve_df], ignore_index=True)
                        
#         # Calculate second derivative ***
#         ### 2nd Derivative updated from apply to transform, review and see how to improve and smooth
#         curve_df['ibts2ndDerivative'] = curve_df.groupby('roastName')['ibtsDerivative'].transform(lambda x: x.diff())
        
#         curve_df.fillna(value=np.nan, inplace=True)
#         return curve_df
    
#     except Exception as e:
#         print("Error: Unable to deconstruct temperature curves.")
#         print("Exception:", str(e))
#         traceback.print_exc()
        
#         #curve_df = pd.DataFrame()
#         return curve_df 

def deconstruct_temp_curves(df):
    try:
        curve_df = pd.DataFrame()
        
        for index, row in df.iterrows():
            # Determine the minimum length among temperature arrays and derivatives
            min_length = min(
                len(row['beanTemperature']), 
                len(row['drumTemperature']), 
                len(row['beanDerivative']), 
                len(row['ibtsDerivative']) if len(row['ibtsDerivative']) > 0 else float('inf')
            )
            
            # Slice all arrays to the minimum length
            bean_temperature = row['beanTemperature'][:min_length]
            drum_temperature = row['drumTemperature'][:min_length]
            bean_derivative = row['beanDerivative'][:min_length]
            
            # Check if 'ibtsDerivative' exists and is not empty
            if len(row['ibtsDerivative']) > 0:
                ibts_derivative = row['ibtsDerivative'][:min_length]
            else:
                # Fill with NaNs if 'ibtsDerivative' is missing
                ibts_derivative = [np.nan] * min_length

            # Create temp_curve_df with temperature and derivative data
            temp_curve_df = pd.DataFrame({
                'beanTemperature': bean_temperature,
                'drumTemperature': drum_temperature,
                'beanDerivative': bean_derivative,
                'ibtsDerivative': ibts_derivative
            })
            
            temp_curve_df['roastName'] = row['roastName']
            temp_curve_df['indexTime'] = temp_curve_df.index
            temp_curve_df['indexFirstCrackStart'] = row['indexFirstCrackStart'] 
            
            # Extract and normalize actionTimeList
            if isinstance(row['actions.actionTimeList'], list) and row['actions.actionTimeList']:
                actions_df = pd.DataFrame(row['actions.actionTimeList'])
                actions_df['type'] = actions_df['ctrlType'].map({0: 'Power', 1: 'Fan', 2: 'Drum'})
                actions_pivot = actions_df.pivot_table(index='index', columns='type', values='value').reset_index()
                
                # Merge actions with temp_curve_df and forward fill
                merged_df = pd.merge(temp_curve_df, actions_pivot, left_on='indexTime', right_on='index', how='left').drop(columns=['index'])
                # Return to the original index
                original_index = merged_df.index

                # Apply groupby, but reset the index before and after the operation to ensure compatibility
                merged_df[['Power', 'Fan', 'Drum']] = (
                    merged_df
                    .reset_index()  # Reset index to default integer index
                    .groupby('roastName')[['Power', 'Fan', 'Drum']]
                    .apply(lambda group: group.ffill().bfill())
                    .reset_index(drop=True)  # Drop the groupby-generated index, revert to default integer index
                )

                # Set the original index back to merged_df  #*** May not be needed unless usign this merged_df elsewhere
                merged_df.index = original_index 
            else:
                temp_curve_df['Power'] = np.nan
                temp_curve_df['Fan'] = np.nan
                temp_curve_df['Drum'] = np.nan
                merged_df = temp_curve_df
            
            # Concatenate with the main curve_df
            curve_df = pd.concat([curve_df, merged_df], ignore_index=True)
                        
        # Calculate second derivative
        curve_df['ibts2ndDerivative'] = curve_df.groupby('roastName')['ibtsDerivative'].transform(lambda x: x.diff())        
        curve_df.fillna(value=np.nan, inplace=True)
        
        # Clean up the columns and types
        curve_df = curve_df[['roastName','indexTime', 'Power', 'Fan', 'Drum','beanTemperature', 'drumTemperature', 'beanDerivative', 'ibtsDerivative', 'ibts2ndDerivative','indexFirstCrackStart']]
        curve_df[['Power', 'Fan', 'Drum']] = curve_df[['Power', 'Fan', 'Drum']].astype({'Power': 'int64', 'Fan': 'int64', 'Drum': 'int64'}, errors='ignore')

        print ("Created temp curves for beanTemperature, drumTemperature, beanDerivative, ibtsDerivative as curve_df via:")
        print("   - Aligned all the temperature data to the same length (some sensors might have different sampling rates)")
        print("   - Processed action lists (changes in power, fan, and drum settings)")
        print("   - Forward-filled missing values (if a setting doesn't change, it carries forward the last known value)")
        print("   - Calculated a second derivative for the IBTS temperature (rate of change of the rate of change)")
        
        return curve_df
    
    except Exception as e:
        print("Error: Unable to deconstruct temperature curves.")
        print("Exception:", str(e))
        import traceback
        traceback.print_exc()
        
        return pd.DataFrame()

def create_point_df(df):
    # Create df of point sets (single entry per profile)
    point_list = ['roastName', 'dateTime', 'beanChargeTemperature', 'beanDropTemperature', 'drumChargeTemperature',
              'drumDropTemperature', 'preheatTemperature', 'roastStartIndex', 'roastEndIndex',
              'weightGreen', 'weightRoasted', 'weightLostPercent', 'ambient', 'humidity', 'Drop-ChargeDeltaTemp',
              'totalRoastTime', 'indexFirstCrackStart', 'indexFirstCrackEnd', 'indexYellowingStart',
              'comments', 'roastNumber', 'firmware', 'missingSeconds', 'rating', 'beanId']
    point_df = pd.DataFrame(df, columns=point_list).reset_index()
    point_df.drop(columns='index', inplace=True)
    
    print (point_df.info())
    point_df.indexYellowingStart = point_df.indexYellowingStart.fillna(value=np.nan)
    point_df.indexFirstCrackStart = point_df.indexFirstCrackStart.fillna(value=np.nan) # needed ? ***

    # Replace bad FC points with np.nan and create firstCrackTime 
    point_df.loc[(point_df.indexFirstCrackStart == 0), 'indexFirstCrackStart'] = np.nan
    point_df.loc[(point_df.indexFirstCrackStart > 10000), 'indexFirstCrackStart'] = np.nan
    point_df['firstCrackTime'] = point_df.indexFirstCrackStart / 60 / 2

    return point_df
    
#12/05/23 fix for firstCrackTime and firstCrackTemp
def calculate_roast_milestone_points(df, point_df):
    for name, group in df.groupby('roastName'):
        minBT = group.beanTemperature.min()
        for i, row in group.iterrows():
            if row.beanTemperature == minBT:  # previously-  and row.beanDerivative >= 0  but a small % of roasts were assigned nan
                point_df.loc[(point_df.roastName == name), 'indexTurningPoint'] = row.indexTime
                point_df.loc[(point_df.roastName == name), 'ibtsTurningPointTemp'] = row.drumTemperature
                break
        for i, row in group.iterrows():
            if row.indexTime > 120 and row.drumTemperature >= 165:
                autoYP165 = row.indexTime
                point_df.loc[(point_df.roastName == name), 'index165PT'] = autoYP165
                break
        if 'indexFirstCrackStart' in group.columns:
            first_crack_start = group['indexFirstCrackStart'].iloc[0]
            if not pd.isna(first_crack_start):
                first_crack_temp = group.loc[group['indexTime'] == first_crack_start, 'drumTemperature'].values[0]
                point_df.loc[point_df['roastName'] == name, 'firstCrackTemp'] = first_crack_temp
            else:
                print(f"No 'indexFirstCrackStart' for roastName: {name}")
        else:
            print(f"No 'indexFirstCrackStart' column in the group for roastName: {name}")
            
    print (''' Calculated the turning point (lowest bean temperature in the roast),
        The time when the drum temperature reaches 165°C,
        The bean temperature at first crack''')
    return point_df
        

def develop_point_df(point_df, curve_df):

    # Create a turningPointTime column to mark the TP time
    sampleRate = 2
    point_df['turningPointTime'] = (point_df.indexTurningPoint) / 60 / sampleRate

 
    #convert WG and WR to numeric values
    point_df['weightGreen'] = pd.to_numeric(point_df['weightGreen'])
    point_df['weightRoasted'] = pd.to_numeric(point_df['weightRoasted'])
    # If weightGreen and weightRoasted are non-zero, calculate weightLostPercent, else set to np.nan
    point_df.loc[(point_df.weightGreen > 0) & (point_df.weightRoasted > 0), 'weightLostPercent'] = (point_df.weightGreen - point_df.weightRoasted) / point_df.weightGreen * 100

    # Replace missing or bad YP pick with autoYP165
    point_df.loc[(point_df.indexYellowingStart < 1), 'indexYellowingStart'] = point_df.index165PT
    point_df.loc[(point_df.indexYellowingStart.isnull()), 'indexYellowingStart'] = point_df.index165PT
    point_df['yellowPointTime'] = point_df.indexYellowingStart / 60 / sampleRate


    # Create a yellowPointTemp165 column to mark the YP temp as 165 always
    point_df['yellowPointTemp165'] = 165
   
    
    ###############
    # # Determine the peakROR for each roastName using an average rolling window
    ###############
    # setting 20  window size  - could adjust to 25 or other? ***
    window_size = 20
    new_df = pd.DataFrame()
    new_df['peakROR'] = curve_df.groupby('roastName')['beanDerivative'].rolling(window=window_size, center=True).mean().groupby(level=0).max()

    # Function to get the indexTime associated with the peak ROR
    def get_max_index_and_time(group):
        rolling_mean = (
            group['beanDerivative']
            .rolling(window=window_size, center=True)
            .mean()
        )
        max_index_time = rolling_mean.nlargest(1).idxmin()
        return pd.Series({
            'roastName': group['roastName'].iloc[0],  # Take the roastName value from the group
            'maxROR25_indexTime': group.loc[max_index_time, 'indexTime']
        })  

    # Apply the custom function to each group
    maxROR_info = curve_df.groupby('roastName').apply(get_max_index_and_time).reset_index(drop=True)

    # Merge new_df with maxROR_info on 'roastName'
    new_df = pd.merge(new_df, maxROR_info, on='roastName', how='left')
    new_df['peakRORTime'] = new_df['maxROR25_indexTime']/2
    new_df = new_df.reset_index(drop=True)
    #merge new_df into point_df based on roastName
    point_df = point_df.merge(new_df[['roastName', 'peakROR', 'peakRORTime']], on='roastName', how='left')
    ###############

    # Time/Temp and Temp/Time calculations for the IBTS drum temp
    point_df['time/temp'] = point_df.totalRoastTime / point_df.drumDropTemperature
    point_df['temp/time'] = point_df.drumDropTemperature / point_df.totalRoastTime
    point_df['Drop-ChargeDeltaTemp'] = point_df.drumDropTemperature - point_df.drumChargeTemperature

    # IBTS BeanProbe difference for change over time plot
    point_df['deltaIBTS-BT-atDrop'] = point_df.drumDropTemperature - point_df.beanDropTemperature


    # Calculate Yellowing Phase Duration, time from Turning point to Yellowing Point
    point_df['yellowingPhaseTime'] = point_df.yellowPointTime - point_df.turningPointTime


    # Calculate Browning Phase Duration, time from Yellowing Point to First Crack Start
    # if first crack time is > 0 calc browning phase, else if firstCrackTime is NaN or blank set browningPhaseTime to NaN
    point_df.loc[(point_df.firstCrackTime.isnull()) | 
        (point_df.firstCrackTime == '') |
        (point_df.firstCrackTime <= 0), 'browningPhaseTime'] = np.nan
    point_df.loc[(point_df.firstCrackTime > 0), 'browningPhaseTime'] = point_df.firstCrackTime - point_df.yellowPointTime


    # Calculate Development Duration, time from First Crack Start to First Crack End or Drop
    # if first crack time is true, run, else if firstCrackTime is NaN or blank set developmentTime to NaN
    point_df.loc[(point_df.firstCrackTime.isnull()) | 
        (point_df.firstCrackTime == '') |
        (point_df.firstCrackTime <= 0), 'developmentTime'] = np.nan
    point_df.loc[(point_df.firstCrackTime > 0), 'developmentTime'] = point_df.totalRoastTime - point_df.firstCrackTime

    # Calculate RoR from Turning Point to Yellowing Point (estimated from straight point to point) *** future TBD - check against the actual mean values from curve_df
    point_df['RoR-yellowing-est'] = (165 - point_df.ibtsTurningPointTemp) / point_df.yellowingPhaseTime


    # Calculate RoR from in the Browing phase (Yellowing Point to First Crack Start)
    # if first crack time is true, run, else if firstCrackTime is NaN or blank set RoR-browning-est to NaN
    point_df.loc[(point_df.firstCrackTime.isnull()) | 
        (point_df.firstCrackTime == '') |
        (point_df.firstCrackTime <= 0), 'RoR-browning-est'] = np.nan
    point_df.loc[(point_df.firstCrackTime > 0), 'RoR-browning-est'] = (point_df.firstCrackTemp - 165) / point_df.browningPhaseTime


    # Calculate RoR from First Crack Start to First Crack End or Drop *** RoR-development-est problem, always = 1
    # if first crack time is true, run, else if firstCrackTime is NaN or blank set RoR-development-est to NaN
    point_df.loc[(point_df.firstCrackTime.isnull()) | 
        (point_df.firstCrackTime == '') |
        (point_df.firstCrackTime <= 0), 'RoR-development-est'] = np.nan
    point_df.loc[(point_df.firstCrackTime > 0), 'RoR-development-est'] = (point_df.totalRoastTime - (point_df.indexFirstCrackStart)/2) / point_df.developmentTime

    # Calculate the fullRoastROR from Turning Point to Drop Temp *** (future fix, this might be better if from Peak ROR to Drop)
    point_df['RoR-fullRoast-est'] = (point_df.drumDropTemperature - point_df.ibtsTurningPointTemp) / (point_df.totalRoastTime - point_df.turningPointTime)

    print("\nCalculated:")
    print("• Weight metrics: green/roasted weights and loss %")
    print(f"• Key phases: Yellowing , Browning, Development times ")
    print("• Temperature metrics: Drop-Charge delta, IBTS-Bean probe difference")
    print("• Rate of Rise (ROR): calculated for yellowing, browning, development, and full roast")
 
    print("\nAssumptions:")
    print("• Sample rate: 2Hz")
    print("• Window size for peak ROR: 20")
    print("• Peak ROR smoothed with rolling average")
    print("• Yellow point fixed at 165°C")
    print("• Missing yellowing points replaced with auto-165°C detection")
    
    return point_df


def check_missing_values(df):
    missing_cols = df.columns[df.isnull().any()].tolist()
    if missing_cols:
        print(f"In the dataframe passed, the following columns have missing values: \n{missing_cols}")
    else:
        print(f"No missing values found in the DataFrame passed.")
