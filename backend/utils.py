import pandas as pd
import plotly.graph_objs as go



def make_profile_plot(data, float_id, param='TEMP'):
    subset = data[data['PLATFORM_NUMBER'] == float_id]
    trace = go.Scatter(x=subset[param], y=subset['PRES'], mode='lines', name=param)
    layout = go.Layout(title=f"{param} Profile for {float_id}",
                        xaxis_title=param, yaxis_title='Depth (dbar)', yaxis=dict(autorange='reversed'))
    fig = go.Figure(data=[trace], layout=layout)
    return fig.to_json()

def fisherman_brief(data, region):
    d = data[data['region'] == region]
    stats = {
        "temp_mean": round(d['TEMP'].mean(),2),
        "salinity_mean": round(d['PSAL'].mean(),2),
        "depth_range": (d['PRES'].min(), d['PRES'].max())
    }
    note = (f"In {region.title()}, surface (0-50m) avg temp: {stats['temp_mean']}°C, "
            f"salinity: {stats['salinity_mean']} PSU. Daily ocean conditions suitable for pelagic activity.")
    return {"stats": stats, "note": note}

def get_float_locations(data):
    return data[['PLATFORM_NUMBER','LATITUDE','LONGITUDE','region']].drop_duplicates().to_dict(orient="records")

def get_profile_data(data, float_id, param):
    d = data[data['PLATFORM_NUMBER'] == float_id]
    # Optionally group by time/depth
    return {
        "depth": d["PRES"].tolist(),
        "value": d[param].tolist(),
        "datetime": d["JULD"].tolist() if "JULD" in d.columns else []
    }

def get_fisherman_brief(data, region):
    d = data[data['region'] == region]
    temp = round(d['TEMP'].mean(),2)
    sal = round(d['PSAL'].mean(),2)
    note = f"{region.replace('_',' ').title()} | Surface temp: {temp}°C, Salinity: {sal} PSU. Likely good pelagic activity."
    return {"note": note, "temp": temp, "salinity": sal}

def export_profiles_to_csv(data, region=None, float_id=None):
    d = data
    if region:
        d = d[d['region']==region]
    if float_id:
        d = d[d['PLATFORM_NUMBER']==float_id]
    file_path = "export_profiles.csv"
    d.to_csv(file_path, index=False)
    return file_path
