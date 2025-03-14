#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 14 09:47:15 2025

@author: ennisk
"""

import xarray as xr
import numpy as np

# Load the already averaged data file with lead times 1-35 in date format
forecast_file_path = '/Path/to/UFS/data/UFS_aug2011_daily_avgs.nc'
forecast_data_SE = xr.open_dataset(forecast_file_path)

# These are the coordinates for the Aug 2011 heat wave case study
locations_SE = {
    'Little Rock, AR': {'lon': 267.72, 'lat': 34.74},
    'New Orleans, LA': {'lon': 269.93, 'lat': 29.95},
    'Asheville, NC': {'lon': 277.45, 'lat': 35.59},
}

# Select forecast dates for LTs 1-20 starting from 07/27 Lt 1
start_date = '2011-07-28'
end_date = '2011-08-16'   # LT 20
selected_dates = np.arange(np.datetime64(start_date), np.datetime64(end_date) + 1)

forecast_data_SE['lon'] = np.where(forecast_data_SE['lon'] > 180, forecast_data_SE['lon'] - 360, 
                                   forecast_data_SE['lon'])

# Create dictionary to store values for each date
temp_values = {city: [] for city in locations_SE.keys()}
dates_list = []

# get 2m- temperature values at case study grid points for each date
for date in selected_dates:
    temp_data = forecast_data_SE['temperature_2m'].sel(time=str(date))
    dates_list.append(str(date))
    
    for city, coords in locations_SE.items():
        temp_value = temp_data.sel(lat=coords['lat'], lon=coords['lon'], method='nearest').item()
        temp_values[city].append(temp_value)

# Create an xarray Dataset to store the values then save to a netcdf. 
temp_ds_SE = xr.Dataset(
    {
        "temperature_2m": ("date", np.array([temp_values[city] for city in locations_SE.keys()]))
    },
    coords={
        "date": dates_list,
        "location": list(locations_SE.keys())
    }
)

output_file = '/Path/to/output/data/UFS_aug2011_LT1_20.nc'
temp_ds_SE.to_netcdf(output_file)

##########################################################################################

## In the second part of this script we do the same as above but for September 2019 Case only

# Load the already averaged data file with lead times 1-35 in date format
forecast_file_path_NW = '/Path/to/UFS/data/UFS_sept2019_daily_avgs.nc'
forecast_data_NW = xr.open_dataset(forecast_file_path_NW)

# These are the coordinates for the Sept 2019 heat wave case study
locations_NW = {
    'Boise, ID': {'lon': 243.80, 'lat': 43.61},
    'Seattle, WA': {'lon': 237.67, 'lat': 47.60},
    'Bend, OR': {'lon': 238.69, 'lat': 44.05},
}

# Select forecast dates for days 1-20 starting from LT 1 
start_date = '2019-08-29'
end_date = '2011-09-17'  # LT 20
selected_dates_NW = np.arange(np.datetime64(start_date), np.datetime64(end_date) + 1)

forecast_data_NW['lon'] = np.where(forecast_data_NW['lon'] > 180, forecast_data_NW['lon'] - 360, 
                                   forecast_data_NW['lon'])

# Create dictionary to store values for each date
temp_values_NW = {city: [] for city in locations_NW.keys()}
dates_list_NW = []

# get 2-m temperature values at case study grid points
for date in selected_dates_NW:
    temp_data_NW = forecast_data_NW['temperature_2m'].sel(time=str(date))
    dates_list_NW.append(str(date))
    
    for city, coords in locations_NW.items():
        temp_value_NW = temp_data_NW.sel(lat=coords['lat'], lon=coords['lon'], method='nearest').item()
        temp_values_NW[city].append(temp_value_NW)

# Create an xarray Dataset to store the values then create a netcdf
temp_ds_NW = xr.Dataset(
    {
        "temperature_2m": ("date", np.array([temp_values_NW[city] for city in locations_NW.keys()]))
    },
    coords={
        "date": dates_list,
        "location": list(locations_NW.keys())
    }
)

output_file_NW = '/Path/to/output/data/UFS_sept2019_LT1_20.nc'
temp_ds_NW.to_netcdf(output_file_NW)