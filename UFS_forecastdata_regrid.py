#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 06:39:52 2024

@author: ennisk
"""

import xarray as xr
import xesmf as xe
import numpy as np

## UFS data for lead times 11-35 if half the grid resolution of the lead times 1-1o files. Lead times 11-35
## are at 0.50x0.50 grid resolution, so this script regrids the UFS data to have it match LTs 1-10 & AIWP

# Load the specific 11-35 data file 
# Here Sept 2019 file is the example
forecast_file_path = '/Path/to/UFS/file/tmp_2m_2019082800.nc'
forecast_data = xr.open_dataset(forecast_file_path)
#extract the temperature variable and convert to Celsius 
temp_2m_forecast = forecast_data['2t'] - 273.15

# Create the new grid with 0.25-degree resolution
ds_out = xr.Dataset(
    {
        'lat': (['lat'], np.arange(-90, 90.25, 0.25)),
        'lon': (['lon'], np.arange(0, 360.25, 0.25)),
    }
)

regridder = xe.Regridder(temp_2m_forecast, ds_out, 'bilinear')
temp_2m_forecast_regridded = regridder(temp_2m_forecast)
ds_regridded = xr.Dataset({'2t': temp_2m_forecast_regridded})

regridded_file_path = '/Path/to/output/tmp_2m_2019082800_regridded.nc'
ds_regridded.to_netcdf(regridded_file_path)

print(f'Regridded data saved to {regridded_file_path}')

## This was run on a GPU to be able to use xesmf regridder & avoid memory overload locally. 
