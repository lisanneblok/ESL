import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature



def plot_variable_at_time(dataset, variable_name, specific_time):
    # Extract data for the specific variable and time
    variable_data = dataset[variable_name].sel(time=specific_time)

    # Plot the variable using Cartopy
    plt.figure(figsize=(10, 6))
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.coastlines()

    # Plot station locations with the variable as color
    scatter = ax.scatter(
        dataset.station_x_coordinate, dataset.station_y_coordinate,
        c=variable_data, cmap='jet', transform=ccrs.PlateCarree())

    # Add color bar
    cbar = plt.colorbar(scatter)
    cbar.set_label(variable_name)

    # Add title and labels
    plt.title(f'{variable_name} at {specific_time}')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')

    plt.show()

def plot_variable_at_box(dataset, variable_name, specific_time, lon_range=(-15, 15), lat_range=(48, 65)):
    # Extract data for the specific variable and time
    variable_data = dataset[variable_name].sel(time=specific_time)

    # Plot the variable using Cartopy
    plt.figure(figsize=(10, 6))
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.coastlines()

    # Set the extent of the plot
    ax.set_extent([lon_range[0], lon_range[1], lat_range[0], lat_range[1]], crs=ccrs.PlateCarree())

    # Plot station locations with the variable as color
    scatter = ax.scatter(
        dataset.station_x_coordinate, dataset.station_y_coordinate,
        c=variable_data, cmap='jet', transform=ccrs.PlateCarree())

    # Add color bar
    cbar = plt.colorbar(scatter)
    cbar.set_label(variable_name)

    # Add title and labels
    plt.title(f'{variable_name} at {specific_time}')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')

    plt.show()


def plot_tide_at_time(selected_data, desired_time):
    # Extract latitude and longitude values from the selected_data xarray dataset
    selected_lon_values = selected_data['longitude'].values
    selected_lat_values = selected_data['latitude'].values

    # Create a figure and axis with a specific projection
    plt.figure(figsize=(10, 6))
    ax = plt.axes(projection=ccrs.PlateCarree())

    # Plot tide at the desired time for selected data
    plt.scatter(selected_lon_values, selected_lat_values, c=selected_data['tide'].sel(time=desired_time).values, cmap='Blues')

    # Add colorbar
    plt.colorbar(label='Tide')

    # Plot land outlines on top
    ax.add_feature(cfeature.LAND, edgecolor='black', zorder=2)

    # Add labels and title
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title(f'Tide at {desired_time}')

    # Show plot
    plt.show()
