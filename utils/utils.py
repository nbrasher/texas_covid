import pandas as pd
import pickle
import boto3
import io
import os
import re

# Texas counties grouped into metro areas
METROS = {
    'Houston': ['Harris', 'Montgomery', 'Fort Bend', 'Brazoria', 'Galveston'],
    'DFW': ['Dallas', 'Tarrant', 'Collin', 'Denton'],
    'Austin': ['Travis', 'Williamson'],
    'San Antonio': ['Bexar'],
    'Amarillo': ['Potter', 'Randall'],
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
    # Set up S3 connection
    s3c = boto3.client(
        's3', 
        region_name = 'us-east-2',
        aws_access_key_id = os.environ['S3_ID'],
        aws_secret_access_key = os.environ['S3_KEY']
    )
    case_file = s3c.get_object(Bucket= 'texas-covid', 
                    Key = 'case_counts.csv')
    results_file = s3c.get_object(Bucket= 'texas-covid', 
                    Key = 'final_results.pkl')


    # Read in raw Daily data
    df = pd.read_csv(io.BytesIO(case_file['Body'].read()),
                     index_col=0)
    
    # Get final computed results
    final_results = pickle.loads(results_file['Body'].read())
    
    return df, final_results

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