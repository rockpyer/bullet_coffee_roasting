# cleaning up the data prior to processing and after processing

def basic_cleanup(df):
    # Sort by time and remove rows with missing roastName
    df.sort_values(by='dateTime', inplace=True)
    df.dropna(subset=['roastName'], inplace=True)

    # Filter dataframe to only your User ID, this removes all the roasts you've saved from other users
    # Find most frequent userID and use that as your choiceUserID
    choiceUserID = df['userId'].value_counts().idxmax()
    #choiceUserID = '73009f59-2d2e-4215-b6ff-961946ee0b80'  # Option to enter your specific userID (extracted from .json roast file, or RoastWorld web address)
    df = df.query('userId == @choiceUserID and isFork != 1.0')

    # Define list of unused data 
    other_meta = ['userId', 'isFork', 'serialNumber', 'IRSensor', 'inventory.nextGreenWeight',
                  'inventory.previousGreenWeight', 'inventory.changeInGreenWeight', 'isPrivate',
                  'slug', 'updated_at', 'updatedAt', 'hardware', 'tagids', 'recipeID',
                  'parentUserId','parentUsername','overlayID', 'actions.actionTempList', 'deviceType']

    # Drop the extra data
    df = df.loc[:, ~df.columns.isin(other_meta)]
    #df.drop(other_meta, axis=1) #not using because this or inplace=True gave errors about setting on a copy
    
    # Shift column 'Name' to first position
    first_column = df.pop('roastName')
    df.insert(0, 'roastName', first_column)
    
    #reset index
    df.reset_index(drop=True, inplace=True)
    
    #print
    print (f'Removed unused columns from RoastTime: {other_meta}')
    
    return df

def fill_derivative_values(df):
    #fill all ibtsDerivative NAN values with 0 (usually just the first 1-2 rows, pretty negligible)
    df['ibts2ndDerivative'] = df['ibts2ndDerivative'].fillna(0)

    #fill all ibtsDerivative values now (usually just the first row and negligible)
    df['ibtsDerivative'] = df['ibtsDerivative'].fillna(0)
    return df

def drop_intermediate_columns(df):
    # *** TBD drop columns that are not needed for analysis in point_df 
    # all index columns, others...
    unneeded = ['roastEndIndex', 'roastStartIndex', 'indexFirstCrackEnd','indexYellowingStart', 'missingSeconds',
                'roastNumber', 'roastDegree', 'tagids', 'recipeID','parentUserId','parentUsername','overlayID', ]
    df = df.loc[:, ~df.columns.isin(unneeded)]

    print (f'Removed potential intermediate columns: {unneeded}')
    return df

def reorder_columns(curve_df):
    # Reorder columns
    curve_df = curve_df[['roastName', 'dateTime', 'indexTime', 'beanTemperature', 'drumTemperature', 'ibtsDerivative', 'ibts2ndDerivative']]
    return curve_df
    