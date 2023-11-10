##############################################################
## simple standalone for accessing your json files as a csv ##

import os
from pathlib import Path
import json
import pandas as pd

# Load from roasTime repository on macOS
home = os.path.expanduser('~')
base_path = os.path.join(home, 'Library/Application Support/roast-time/roasts')
##  IF you have a specific set of roast profiles in another folder, uncomment the below
# base_path = Path('/data')

df = pd.DataFrame()

for entry in os.listdir(base_path):
    full_path =  Path('%s/%s' % (base_path, entry))
    with full_path.open() as f:
        data = json.loads(f.read())
        df_load = pd.json_normalize(data)
    df = pd.concat([df,df_load], ignore_index=True)

# Export the raw DataFrame to a .csv file just for the record
#create subfolder
subfolder = 'csvExports/'
if not os.path.exists(subfolder):
    os.makedirs(subfolder)

df.to_csv(subfolder + f"raw_bullet-roasting_df.csv", index=False)