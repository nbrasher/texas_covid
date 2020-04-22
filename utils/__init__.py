from datetime import datetime
import pandas as pd
import pickle
import os
import re

# Calculate for 12 counties with highest case counts
INCLUDE_COUNTIES = [
    'Harris',
    'Dallas',
    'Tarrant',
    'Travis',
    'Bexar',
    'Fort Bend',
    'Denton',
    'El Paso',
    'Collin',
    'Galveston',
    'Lubbock',
    'Montgomery'
]

def load_cases():
    ''' Read in raw Excel data
    '''
    # Read in raw Daily data
    df = pd.read_excel(os.path.join('data', 'Texas COVID-19 Case Count Data by County.xlsx'),
                    skiprows=2,
                    nrows=254, 
                    index_col='County Name')

    # Drop population column and parse date headers
    if 'Population' in df.columns:
        df = df.drop('Population', axis=1)
        
    if df.columns.dtype == 'O':
        date_idx = [datetime.strptime(
                        '2020-'+re.search(r'\n(.+)', c)[1],
                        '%Y-%m-%d'
                    )
                    for c in df.columns]
        df.columns = date_idx
    
    # Get final computed results
    with open(os.path.join('data', 'final_results.pkl'), 'rb') as f:
        final_results = pickle.load(f)
    
    return df, final_results