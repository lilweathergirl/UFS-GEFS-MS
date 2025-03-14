#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 06:35:53 2024

@author: ennisk
"""

import xarray as xr
import numpy as np

# Define file paths for forecast files for LTs 1-10 & 11-35
# These forecast files are for the August 2011 SE heat wave event specifically. 
# UFS initalizes their forecasts every seven days starting 1-05-2000
forecast1_10 = '/Path/to/my/UFS_File/tmp_2m_2011072700.nc'
forecast11_35 = '/Path/to/my/UFS_File/tmp_2m_2011072700.nc'

# Load in both datasets since UFS GEFS has their forecast lead times in separate files. 
# Lead times 1-10 are in one file and 11-35 in another. 
# Instead of merging the two data sets prior to averaging, I do it after 
ds1_10 = xr.open_dataset(forecast1_10)
ds11_35 = xr.open_dataset(forecast11_35)

# 6-hourly time steps at 00Z, 06Z, 12Z, and 18Z 
ds1_10 = ds1_10.sel(time=ds1_10['time'].dt.hour.isin([0, 6, 12, 18]))
ds11_35 = ds11_35.sel(time=ds11_35['time'].dt.hour.isin([0, 6, 12, 18]))

# Convert the temperatures from Kelvin to Celsius
ds1_10['2t'] = ds1_10['2t'] - 273.15
ds11_35['2t'] = ds11_35['2t'] - 273.15

# Create a valid forecast date based on initialization + lead times
# UFS data forecasts at a specific date and time and provides forecasts in time steps 
# (lead times). Each forecast time is tied to a specific date that forecast is valid for. 
# Valid time ensures each forecast date at each time step is correctly represented, and
# therefore averaged correctly. 
ds1_10 = ds1_10.assign_coords(valid_time=ds1_10['time'])
ds11_35 = ds11_35.assign_coords(valid_time=ds11_35['time'])

# Compute 6-hourly averages for each forecast file
# This ensures each 6-hr time step for the same forecast date is averaged together 
temp_avg_1_10 = ds1_10.groupby("valid_time.date").mean(dim="valid_time")
temp_avg_11_35 = ds11_35.groupby("valid_time.date").mean(dim="valid_time")

# Merge all the lead times into one file. 
# I only need lead times 1-20, however, I am doing the full 1-35 for simplicity and will extract only
# lead times 1-20 later when needing grid point / region average values. 
temp_avg_combined = xr.concat([temp_avg_1_10, temp_avg_11_35], dim='date')
output_file = '/Path/to/output/data/UFS_aug2011_daily_avgs.nc'
temp_avg_combined.to_netcdf(output_file)

