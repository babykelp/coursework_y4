import pandas as pd
import numpy as np
import os
from netCDF4 import Dataset

def convert_time_to_model_format(time_index):
    return [float(time.strftime("%Y%m%d") + f"{(time.hour/24 + time.minute/(24*60) + time.second/(24*60*60)):.4f}".lstrip('0')) for time in time_index]

# Read the excel data skipping the unit row
df = pd.read_excel('/home/babykelp/eccc/2019+Qinghai Lake basin observatory network+JJC+AWS.xlsx', skiprows=[1])

# Replace -6999 with NaN
df.replace(-6999, np.nan, inplace=True)

# Forward fill NaN values
df.ffill(inplace=True)

# If there are any remaining NaNs (e.g., at the start of the dataset), backward fill
df.bfill(inplace=True)

# Convert specific columns
df['Rain'] = df['Rain'] / (1000 * 3600)  # Convert from mm to kgm-2s-1
df['Press'] = df['Press'] * 100  # Convert from hPa to Pa

# Rename columns
df = df.rename(columns={
    'TIMESTAMP': 'time',
    'DR': 'ds',
    'DLR_Cor': 'dl',
    'Rain': 'pre',
    'Ta_3m': 'tmp',
    'RH_3m': 'spfh',
    'WS_3m': 'wind',
    'Press': 'pres'
})

# Set 'time' as index and convert it to datetime
df.set_index('time', inplace=True)
df.index = pd.to_datetime(df.index)

# 
##
### TO MAKE FAKE TIME INDEX SO THE NEW METEOROLOGY WOULD WORK WITH CN-Dan station init file we need to choose a year before 2018
# df.index = df.index - pd.DateOffset(years=(df.index[0].year - 2002))
##
#

agg_dict = {
    'ds': 'mean',
    'dl': 'mean',
    'pre': 'sum',
    'tmp': 'mean',
    'spfh': 'mean',
    'wind': 'mean',
    'pres': 'mean'
}

# df = df.resample('h').agg(agg_dict)
# Extract start and end year
start_year = df.index.min().year
end_year = df.index.max().year

# Make directory if it does not exist
if not os.path.exists('CLASSIC/inputFiles/Qinghai_Lake'):
    os.makedirs('CLASSIC/inputFiles/Qinghai_Lake')


# Dictionary with units
units_dict = {
    'ds': 'Wm^-2',
    'dl': 'Wm^-2',
    'pre': 'kgm-2s-1',
    'tmp': 'degree C',
    'spfh': 'kgkg^-1',
    'wind': 'ms^-1',
    'pres': 'Pa'
}

for variable in ['ds', 'dl', 'pre', 'tmp', 'spfh', 'wind', 'pres']:
    ncfile = Dataset(f'CLASSIC/inputFiles/Qinghai_Lake/{variable}_{end_year}.nc', mode='w', format='NETCDF4')

    # Create dimensions
    time_dim = ncfile.createDimension('time', None)  # Unlimited dimension
    lat_dim = ncfile.createDimension('lat', 1)
    lon_dim = ncfile.createDimension('lon', 1)

    # Create variables
    var = ncfile.createVariable(variable, 'f4', ('time', 'lat', 'lon'), fill_value=9.96921e+36)
    lat_var = ncfile.createVariable('lat', 'f4', ('lat',))
    lon_var = ncfile.createVariable('lon', 'f4', ('lon',))
    time_var = ncfile.createVariable('time', 'f8', ('time',))

    # Convert time index to the required format
    time_values = convert_time_to_model_format(df.index)

    # Assign values to dimensions
    var[:, 0, 0] = df[variable].values
    lat_var[0] = 37.25
    lon_var[0] = 100.24
    time_var[:] = time_values

    # Set attributes
    ncfile.setncattr("title", f"{variable} data")
    var.setncattr('long_name', variable)
    var.setncattr('units', units_dict.get(variable, 'unknown'))
    var.setncattr('missing_value', 9.96921e+36)

    lat_var.setncattr('standard_name', 'latitude')
    lat_var.setncattr('long_name', 'latitude')
    lat_var.setncattr('units', 'degrees_north')
    lat_var.setncattr('axis', 'Y')

    lon_var.setncattr('standard_name', 'longitude')
    lon_var.setncattr('long_name', 'longitude')
    lon_var.setncattr('units', 'degrees_east')
    lon_var.setncattr('axis', 'X')

    time_var.setncattr('standard_name', 'time')
    time_var.setncattr('units', 'day as %Y%m%d.%f')
    time_var.setncattr('calendar', 'proleptic_gregorian')
    time_var.setncattr('axis', 'T')

    ncfile.close()
    
    #use cdo library code in the directory of outputs then
    # for file in *9.nc;  
    # do echo $file;  
    # cdo settaxis,2019-01-01,00:00:00,10min $file ${file}_corr.nc; 
    # done