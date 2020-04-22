from datetime import datetime
from scipy import stats
import pandas as pd
import numpy as np
import pickle
import os
import re

# Array for all possible values of Rt
R_T_MAX = 6
r_t_range = np.linspace(0, R_T_MAX, R_T_MAX*100+1)

# Gamma is 1/serial interval
# https://wwwnc.cdc.gov/eid/article/26/7/20-0282_article
# https://www.nejm.org/doi/full/10.1056/NEJMoa2001316
GAMMA = 1/7

# Base sigma from ongoing analysis is ~0.3
SIGMA = 0.3

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

def prepare_cases(cases, min_cases=20):
    ''' Calculate rolling 7-day moving average of new cases

        Parameters:
            cases (pd.Series): Time series of new cases
            min_cases (int): Minimum number of average new cases to consider
        
        Returns:
            original (pd.Series): Original case counts with index starting
            when rolling average cases is greater than min_cases
            smoothed (pd.Series): 7-day rolling average of new cases
    '''
    new_cases = cases.diff()

    smoothed = new_cases.rolling(7,
        win_type='gaussian',
        min_periods=1,
        center=True).mean(std=2).round()
    
    idx_start = np.searchsorted(smoothed, min_cases)
    
    smoothed = smoothed.iloc[idx_start:]
    original = new_cases.loc[smoothed.index]
    
    return original, smoothed