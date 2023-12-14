# This file contains functions for loading roasting data
# typically from the roasTime repository on macOS, or for loading the data from a specific folder.
import os
from pathlib import Path
import json
import pandas as pd

def load_roasting_data(base_path):
    df = pd.DataFrame()
    for entry in os.listdir(base_path):
        full_path = Path('%s/%s' % (base_path, entry))
        with full_path.open() as f:
            data = json.loads(f.read())
            df_load = pd.json_normalize(data)
        df = pd.concat([df, df_load], ignore_index=True)
    return df
