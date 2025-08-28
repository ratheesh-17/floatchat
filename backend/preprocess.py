import xarray as xr
import os
import pandas as pd

regions = ["arabian_sea", "bay_of_bengal", "indian_ocean"]
data_list = []
for region in regions:
    folder = fr"C:/Users/91934/floatchat/data/{region}/"
    for filename in os.listdir(folder):
        if filename.endswith(".nc"):
            ds = xr.open_dataset(os.path.join(folder, filename))
            df = ds.to_dataframe().reset_index()
            df['region'] = region  # tag for later filtering
            data_list.append(df)
all_data = pd.concat(data_list, ignore_index=True)
all_data.to_parquet(r"C:/Users/91934/floatchat/argo_profiles.parquet")



