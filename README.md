# Texas Covid
Evaluation of Rt for each Texas County using Kevin Systrom's methodology as described in [this notebook](https://github.com/k-sys/covid-19/blob/master/Realtime%20R0.ipynb) and deployed at [Rt.live](https://rt.live/)

## Setup Instructions
Download recent case count data with  `curl -o data/Texas\ COVID-19\ Case\ Count\ Data\ by\ County.xlsx https://dshs.texas.gov/coronavirus/TexasCOVID19DailyCountyCaseCountData.xlsx`

### Jupyter Setup
1. Create a virtual environment with `conda env create -f requirements.yml`
1. Launch Jupyter with `jupyter lab`
- In order to integrate plotly into the jupyter build follow [these instructions](https://plotly.com/python/getting-started/#jupyterlab-support-python-35)

### Dash Setup
In order to run the Dash App:
1. Install requirements with `pip install -r requirements.txt` (or use conda as above)
1. Launch the App with `python app.py`