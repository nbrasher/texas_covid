from datetime import datetime
import pandas as pd
import pickle
import boto3
import io
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

        Returns:
            df (pd.DataFrame): DataFrame of total Texas covid-19 cases by county and day
            final_results (dict[Str: pd.DataFrame]): Dict with keys as county names, 
                values as DataFrame of most likely Rt and 80% confidence bounds by day
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
                     index_col='County Name')
    
    # Get final computed results
    final_results = pickle.loads(results_file['Body'].read())
    
    return df, final_results