#### Data loading for Allio Bullet R1 V2 roaster https://aillio.com/?page_id=23112
###### Coffee Roasting by Ryan @f.w.Bennies https://www.instagram.com/f.w.bennies/

### Key Edits for you to run this = Lines 16-19 set to the bullet roast file location for your machine

#################################################
## open each .json in folder and append to df  ##
#################################################

from pathlib import Path
import os
import pandas as pd
import json
from datetime import datetime


# Load from roasTime repository on macOS
home = os.path.expanduser('~')
base_path = os.path.join(home, 'Library/Application Support/roast-time/roasts')
df = pd.DataFrame()

for entry in os.listdir(base_path):
    full_path =  Path('%s/%s' % (base_path, entry))
    with full_path.open() as f:
        data = json.loads(f.read())
        df_load = pd.json_normalize(data)
    df = df.append(df_load)
df.sort_values(by='dateTime', inplace = True)
df = df.reset_index()
df = df.drop(columns = ['index'])

# converting dataTime to useful format
df['dateTime'] = pd.to_datetime(df['dateTime'],unit='ms')