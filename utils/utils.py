from google.cloud import firestore
from datetime import datetime
import pandas as pd
import pickle

# Texas counties grouped into metro areas
METROS = {
    'Houston': ['Harris', 'Montgomery', 'Fort Bend', 'Brazoria', 'Galveston'],
    'Dallas Fort Worth': ['Dallas', 'Tarrant', 'Collin', 'Denton'],
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
    db = firestore.Client()
    collection_ref = db.collection("model-results")
    query = collection_ref.order_by(
        "updated", direction=firestore.Query.DESCENDING
    ).limit(1).stream()
    query_output = [d.to_dict() for d in query]

    doc = query_output[0]
    doc.pop("created")
    timestamp = doc.pop("updated")
    timestring = datetime.fromtimestamp(timestamp).strftime('%b %d, %-I:%M %p CT')

    results = {
        k.replace("_", " ").title(): pd.DataFrame(data=v).set_index("date")
        for k, v in doc.items()
    }

    return timestring, results

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
