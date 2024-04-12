import os
import matplotlib.pyplot as plt
import xarray as xr


def find_nc_files(folder_path):
    nc_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.nc'):
                nc_files.append(os.path.join(root, file))
    return nc_files

def open_files(folder_path):
    # Find all .nc files within folders and subfolders
    nc_files_list = find_nc_files(folder_path)
    # Open all files in nc_files_list as one xarray dataset
    combined_dataset = xr.open_mfdataset(
        nc_files_list, combine='nested', concat_dim='time', engine='netcdf4')
    return combined_dataset

def find_varnc_files(folder_path):
    nc_files_by_variable = {}
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.nc'):
                nc_file = os.path.join(root, file)
                variable_name = os.path.basename(nc_file).split('_')[0].split('-')[1]
                if variable_name not in nc_files_by_variable:
                    nc_files_by_variable[variable_name] = []
                nc_files_by_variable[variable_name].append(nc_file)
    return nc_files_by_variable


def load_datasets(folder_path):
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

def store_datasets_in_globals(folder_path):
    # Load datasets from the specified folder path
    datasets = load_datasets(folder_path)
    
    # Store datasets in the global scope
    for variable_name, dataset in datasets.items():
        # Create a variable with the same name as the variable_name and assign the dataset to it
        globals()[variable_name + '_dataset'] = dataset

# Example usage:
# store_datasets_in_globals(folder_path)
# Now you can access each dataset using its variable name globally, e.g., mwd_dataset, wdw_dataset, etc.


def separate_datasets(folder_path):
    nc_files_by_variable = find_varnc_files(folder_path)

    # Iterate over variable names
    for variable_name, files in nc_files_by_variable.items():
        # Open all files combined using xr.open_mfdataset
        combined_dataset = xr.open_mfdataset(files)
    
        # Create a variable with the same name as the variable_name and assign the dataset to it
        globals()[variable_name + '_dataset'] = combined_dataset

    # List out the names of the datasets
    dataset_names = [name for name in globals() if name.endswith('_dataset')]

    # Print out the list of dataset names
    print("Available datasets:")
    for name in dataset_names:
        print(name)

    return dataset_names

