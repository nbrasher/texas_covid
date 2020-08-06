from google.cloud.storage import Client
import pandas as pd
import pickle
import io
import os
import re

# Texas counties grouped into metro areas
METROS = {
    'Houston': ['Harris', 'Montgomery', 'Fort Bend', 'Brazoria', 'Galveston'],
    'DFW': ['Dallas', 'Tarrant', 'Collin', 'Denton'],
    'Austin': ['Travis', 'Williamson'],
    'San Antonio': ['Bexar'],
    'San Marcos': ['Hays'],
    'El Paso': ['El Paso'],
    'Rio Grande Valley': ['Hidalgo', 'Cameron'],
    'Lubbock': ['Lubbock'],
}

def load_cases():
    ''' Read in raw case counts and model output from S3

        Returns:
            df (pd.DataFrame): DataFrame of total Texas covid-19 cases by county
            final_results (dict[str: pd.DataFrame]): Dict with keys as county names, 
                values as DataFrame of Rt and 80% confidence bounds by day
    '''
    # Download file from cloud storage
    bucket = Client().bucket('texas-covid.appspot.com')
    bucket.blob('final_results.pkl').download_to_filename('/tmp/final_results.pkl')

    # Get final computed results
    with open('/tmp/final_results.pkl', 'rb') as f:
        final_results = pickle.load(f)

    return final_results

def areas_to_string(area):
    ''' Return a string describing county makeup of metro areaa

        Parameters:
            area (str): metro area name

        Returns:
            description (str): Description of counties contained in area
    '''

    assert area in METROS.keys(), f'{area} is an invalid area name'

    if len(METROS[area]) < 2:
        return f'The **{area}** area view includes data from {METROS[area][0]} county'
    else:
        return f"The **{area}** area view includes data from {', '.join(METROS[area][:-1])} and {METROS[area][-1]} counties"