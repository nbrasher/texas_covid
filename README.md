# Texas Covid
This app provides a view of the realtime reproduction number (Rt) of the covid-19 epidemic in Texas at the County level. The underlying model uses Kevin Systrom's methodology as described in [this notebook](https://github.com/k-sys/covid-19/blob/master/Realtime%20Rt%20mcmc.ipynb) and deployed at [Rt.live](https://rt.live/). 

## Setup Instructions
The app downloads case count and model output from S3. For raw case count data go to the [Texas DSHS](https://dshs.texas.gov/coronavirus/) webpage.

In order to run the Dash app locally:
1. Install requirements with `pip install -r requirements.txt`
1. Launch the App with `python main.py`

To deploy to GCP
1. Authenticate and set project
1. Deploy with `gcloud app deploy`