from fastapi import FastAPI, Query
import pandas as pd
from utils import get_float_locations, make_profile_plot, fisherman_brief
from config import DATA_PATH

app = FastAPI(title='Argo Float Ocean API')
data = pd.read_parquet(DATA_PATH)

@app.get("/")
def root():
    return {"msg":"ARGO Float API OK"}

@app.get("/float_locations")
def float_locations():
    return get_float_locations(data)

@app.get("/profiles")
def get_profiles(float_id: str = None, region: str = None):
    d = data
    if float_id:
        d = d[d['PLATFORM_NUMBER'] == float_id]
    if region:
        d = d[d['region'] == region]
    return d.head(100).to_dict(orient="records")

@app.get("/profile_plot")
def profile_plot(float_id: str, param: str = "TEMP"):
    return make_profile_plot(data, float_id, param)

@app.get("/fisherman_brief")
def fisherman_summary(region: str = "arabian_sea"):
    return fisherman_brief(data, region)
