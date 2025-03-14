#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 08:04:23 2024

@author: ennisk
"""

import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.io import shapereader
from shapely.ops import unary_union
from shapely.vectorized import contains
import shapely.vectorized

# Load in the already averaged data file with lead times 1-35 in date format
forecast_file_path = '/Path/to/UFS/data/UFS_aug2011_daily_avgs.nc'
forecast_data = xr.open_dataset(forecast_file_path)

# These are the coordinates for the August 2011 SE heat wave case study
locations = {
    'Little Rock, AR': {'lon': 267.72, 'lat': 34.74},
    'New Orleans, LA': {'lon': 269.93, 'lat': 29.95},
    'Asheville, NC': {'lon': 277.45, 'lat': 35.59},
}

# selecting a forecast date (first day of heat wave as example here: daily average already in file)
forecast_date = '2011-08-03'
temp_data = forecast_data['temperature_2m'].sel(time=forecast_date)

# Southeast U.S. states: for finding regional average/ plotting over the SE only
SE_state_names = ['Florida', 'Georgia', 'South Carolina', 'North Carolina', 'Alabama', 'Louisiana', 
                  'Mississippi', 'Arkansas', 'Tennessee', 'Kentucky', 'Virginia']

# Using Natural Earth to get the state geoms
shpfilename = shapereader.natural_earth(resolution='10m', category='cultural', name='admin_1_states_provinces')
states_shp = shapereader.Reader(shpfilename)
se_states_geom = unary_union([state.geometry for state in states_shp.records() if state.attributes['name'] in SE_state_names])

# Extract latitude and longitude values
lons = forecast_data.lon.values
lats = forecast_data.lat.values
if lons.ndim == 1 and lats.ndim == 1:
    lon_grid, lat_grid = np.meshgrid(lons, lats)
else:
    lon_grid, lat_grid = lons, lats

temp_data['lon'] = np.where(temp_data['lon'] > 180, temp_data['lon'] - 360, temp_data['lon'])
lon2d, lat2d = np.meshgrid(temp_data['lon'].values, temp_data['lat'].values)

# Masking the temperature data for the Southeast states only
mask_se_states = shapely.vectorized.contains(se_states_geom, lon2d, lat2d)
temp_masked = temp_data.where(mask_se_states)

# Compute the SE region average 2m-temperature 
southeast_avg_temp = temp_masked.mean().item()
print(f'Southeast Average Temperature on {forecast_date}: {southeast_avg_temp:.2f}°C')

# Plotting steps: 

color_min, color_max = 15, 41  
color_bins = np.linspace(color_min, color_max, 60)

fig, ax = plt.subplots(figsize=(16, 9), dpi=800, subplot_kw={'projection': ccrs.PlateCarree()})
ax.add_feature(cfeature.OCEAN, facecolor='lightgray')
ax.set_facecolor('lightgray')
ax.add_feature(cfeature.COASTLINE.with_scale('10m'))
ax.add_feature(cfeature.BORDERS.with_scale('10m'), linestyle=':')
ax.add_feature(cfeature.STATES.with_scale('10m'), edgecolor='black')

# Plotting the masked temperature data: 
temp_plot = temp_masked.plot.contourf(
    ax=ax, cmap='YlOrRd', extend='both', levels=color_bins, add_colorbar=False, transform=ccrs.PlateCarree()
)

# Add my SE grid point locations onto map 
for city, coords in locations.items():
    ax.scatter(coords['lon'], coords['lat'], color='black', marker='*', s=280, label=city, zorder=5)

cbar = fig.colorbar(temp_plot, ax=ax, orientation='vertical', pad=0.03)
cbar.set_label('Temperature (°C)', fontsize=24, labelpad=22)
cbar.set_ticks(np.arange(color_min, color_max + 1, 5))
cbar.ax.tick_params(labelsize=23)

# Title: this script allows for looking at one lead time at a time during this particular heat wave to be able to plot 2-m temp.
# spatially to see the varying differences in temperature prediction to compare to AI and ERA5
ax.set_title('UFS Forecast 2m Temperature for Lead time 7: August 2011 Southeast Heatwave', fontsize=22)
plt.tight_layout()
plt.show()




