# Origin and roast count lookup, replacing the old OpenAI call in src/AI.py
# Origin comes from the bean record each roast links to (beanId -> beans/<uid>.json 'country').
# Roasts with no linked bean (or a bean with no country) fall back to a keyword match on roastName.
import os
import re
import json
import pandas as pd

# Checked in order, first match wins. 'blend' is first so mixed-origin roasts aren't tagged with one country.
ORIGIN_KEYWORDS = [
    ('blend', 'Blend'),
    ('ethiop', 'Ethiopia'),
    ('eth ', 'Ethiopia'),
    ('yirg', 'Ethiopia'),
    ('guat', 'Guatemala'),
    ('kenya', 'Kenya'),
    ('salvador', 'El Salvador'),
    ('colombia', 'Colombia'),
    ('columbia', 'Colombia'),
    ('rwanda', 'Rwanda'),
    ('papua', 'Papua New Guinea'),
    ('png', 'Papua New Guinea'),
    ('sumatra', 'Indonesia'),
    ('java', 'Indonesia'),
    ('indonesia', 'Indonesia'),
    ('burundi', 'Burundi'),
    ('nicaragua', 'Nicaragua'),
    ('peru', 'Peru'),
    ('brazil', 'Brazil'),
    ('honduras', 'Honduras'),
]


def load_bean_countries(beans_path):
    # Map bean uid -> country from the RoasTime beans folder
    countries = {}
    for entry in os.listdir(beans_path):
        full_path = os.path.join(beans_path, entry)
        if not os.path.isfile(full_path):
            continue
        try:
            with open(full_path) as f:
                bean = json.load(f)
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue
        if bean.get('uid') and bean.get('country'):
            countries[bean['uid']] = bean['country']
    return countries


def origin_from_name(roast_name):
    name = f' {roast_name.lower()} '
    for keyword, country in ORIGIN_KEYWORDS:
        if keyword in name:
            return country
    return None


def roast_count_from_name(roast_name):
    # The roast number follows the # symbol, e.g. "#48 Eth Yirgacheffe 3rd" -> 48
    match = re.search(r'#\s*(\d+)', roast_name)
    return int(match.group(1)) if match else None


def add_origin_and_roast_count(point_df, beans_path):
    bean_countries = load_bean_countries(beans_path)
    point_df['Origin'] = [
        bean_countries.get(bean_id) or origin_from_name(name)
        for bean_id, name in zip(point_df['beanId'], point_df['roastName'])
    ]
    point_df['roastCount'] = point_df['roastName'].apply(roast_count_from_name).astype('Int64')

    missing = point_df.loc[point_df['Origin'].isnull(), 'roastName'].tolist()
    print(f"Origin set for {point_df['Origin'].notnull().sum()} of {len(point_df)} roasts (bean record first, roastName keywords as fallback)")
    if missing:
        print(f"   - No origin found for: {missing}")
    return point_df
