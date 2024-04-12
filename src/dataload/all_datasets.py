import os
import xarray as xr
import sys
sys.path.append('/Users/lb962/Downloads/ESL/GESLA/')
from src.dataload.dataloader import find_varnc_files


def open_CODEC(data_folder):
    # Path to the tide NetCDF files
    CODEC_folder = "data/processed/CODEC/"
    folder_path = os.path.join(data_folder, CODEC_folder)
    # List of .nc files in the folder
    files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.nc')]

    # Open each file individually and store them in a list
    datasets = [xr.open_dataset(file) for file in files]

    return datasets


def wave_datasets(data_folder):
    wave_folder = "data/ERA5waves"
    folder_path = os.path.join(data_folder, wave_folder)

    nc_files_by_variable = find_varnc_files(folder_path)
    datasets = {}
    
    # Iterate over variable names
    for variable_name, files in nc_files_by_variable.items():
        # Open all files combined using xr.open_mfdataset
        combined_dataset = xr.open_mfdataset(files)
        
        # Store the dataset in the dictionary with the variable name as the key
        datasets[variable_name] = combined_dataset

    # Return the dictionary containing datasets
    return datasets

def ERA5_datasets(data_folder):
    # Define the path to the folder containing the NetCDF files
    folder_path = os.path.join(data_folder, 'data/ERA5hourly')

    # Get a list of all NetCDF files in the folder
    nc_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.nc')]

    # Open all NetCDF files as a single xarray Dataset
    ERA5_dataset = xr.open_mfdataset(nc_files)
    return ERA5_dataset


def CMIP6_datasets(data_folder, lon_min, lon_max, lat_min, lat_max):
    # List to store selected data
    selected_datasets = []

    # List of file names for the six files
    file_names = ['HAT', 'LAT', 'MHHW', 'MLLW', 'MSL', 'TR']

    # Loop over each file
    for file_name in file_names:
        # Open the NetCDF file
        CMIP6_path = f"data/API_calls/CMIP6_50/historical_tide_actual-value_1985-2014_{file_name}_v1.nc"
        file_path = os.path.join(data_folder, CMIP6_path)
        dataset = xr.open_dataset(file_path)

        # Rename station_y_coordinate to latitude and station_x_coordinate to longitude
        dataset = dataset.rename({'station_y_coordinate': 'latitude', 'station_x_coordinate': 'longitude'})

        # Extract longitude and latitude coordinates
        lon_values = dataset['longitude'].values
        lat_values = dataset['latitude'].values

        # Boolean indexing to select the desired range
        selected_indices = (lon_values >= lon_min) & (lon_values <= lon_max) & (lat_values >= lat_min) & (lat_values <= lat_max)

        # Select the data based on the indices
        selected_data = dataset.isel(stations=selected_indices)

        # Append selected data to the list
        selected_datasets.append(selected_data)

    # Concatenate the datasets along the stations dimension
    combined_dataset = xr.concat(selected_datasets, dim='stations')

    return combined_dataset
