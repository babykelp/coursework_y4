import xarray as xr
import numpy as np

# Creating coordinates for dimensions
coords = {
    "tile": (["tile"], [1]),
    "lat": (["lat"], [37.25]),
    "lon": (["lon"], [100.24]),
    "ic": (["ic"], range(1, 5)),
    "layer": (["layer"], range(1, 8)),
    "icp1": (["icp1"], range(1, 6))
}

# Creating a dataset with the above coordinates
ds = xr.Dataset(coords=coords)

# Function to create a variable with additional attributes
def create_variable(data, dims, fill_value, units, long_name, **additional_attrs):
    attrs = {
        "_FillValue": fill_value,
        "units": units,
        "long_name": long_name,
    }
    attrs.update(additional_attrs)  # Adding any additional attributes
    return xr.DataArray(
        data,  # Using the provided data instead of fill_value
        coords={dim: ds[dim].values for dim in dims},
        dims=dims,
        attrs=attrs
    )

variables = {
    "ALBS": create_variable(np.full((1, 1, 1), 0.00), ["tile", "lat", "lon"], -999.0, "kg/kg", "Snow albedo"),
    "ALIC": create_variable(np.full((1, 5, 1, 1), -999.00), ["tile", "icp1", "lat", "lon"], -999.0, "kg/kg", "Average near-IR albedo of vegetation category when fully-leafed"),
    "ALVC": create_variable(np.full((1, 5, 1, 1), -999.00), ["tile", "icp1", "lat", "lon"], -999.0, "kg/kg", "Average visible albedo of vegetation category when fully-leafed"),
    "CLAY": create_variable(np.full((1, 7, 1, 1), -999.00), ["tile", "layer", "lat", "lon"], -999.0, "%", "Percentage clay content, Dai et al.,2020"),
    # "CMAI": create_variable(np.full((1, 4, 1, 1), 0), ["tile", "ic", "lat", "lon"], -999.0, "kg m^{-2}", "Annual maximum canopy mass for vegetation category"),
    "CMAS": create_variable(np.full((1, 4, 1, 1), -999.00), ["tile", "ic", "lat", "lon"], -999.0, "kg m^{-2}", "Annual maximum canopy mass for vegetation category"),
    "DELZ": create_variable(np.full(7, 0.1), ["layer"], -999.0, "m", "Ground layer thickness, Dai et al.,2020"),
    "DRN": create_variable(np.full((1, 1, 1), 0.005), ["tile", "lat", "lon"], -999.0, "-", "Soil drainage index"),
    "FARE": create_variable(np.full((1, 1, 1), 1.00), ["tile", "lat", "lon"], -999.0, "fraction", "Tile fractional area of gridcell"),
    "FCAN": create_variable(np.full((1, 5, 1, 1), 0.00), ["tile", "icp1", "lat", "lon"], -999.0, "-", "Annual maximum fractional coverage of modelled area (read in for CLASS only runs)"),
    "GC": create_variable(np.full((1, 1), -1.00), ["lat", "lon"], -999, "-", "GCM surface descriptor - land surfaces (inc. inland water) is -1"),
    "GRO": create_variable(np.full((1, 1, 1), 0.00), ["tile", "lat", "lon"], -999.0, "-", "Vegetation growth index"),
    "GROROT": create_variable(np.full((1, 1, 1), 0.00), ["tile", "lat", "lon"], -999.0, "-", "Vegetation growth index"),
    "LNZ0": create_variable(np.full((1, 5, 1, 1), -999.00), ["tile", "icp1", "lat", "lon"], -999.0, "-", "Natural logarithm of maximum vegetation roughness length"),
    "MID": create_variable(np.full((1, 1), 1.00), ["lat", "lon"], -999, "-", "Mosaic tile type identifier (1 for land surface, 0 for inland lake)"),
    "ORGM": create_variable(np.full((1, 7, 1, 1), -999.00), ["tile", "layer", "lat", "lon"], -999.0, "%", "Percentage organic matter content, Dai et al.,2020"),
    "PAMN": create_variable(np.full((1, 4, 1, 1),-999.00), ["tile", "ic", "lat", "lon"], -999.0, "-", "Annual minimum plant area index of vegetation category"),
    "PAMX": create_variable(np.full((1, 4, 1, 1), -999.00), ["tile", "ic", "lat", "lon"], -999.0, "-", "Annual maximum plant area index of vegetation category"),
    # "QAC": create_variable(np.full((1, 1, 1), 44.42), ["tile", "lat", "lon"], -999.0, "-", "Specific humidity of air within vegetation canopy space [kgkg−1]"),
    "RCAN": create_variable(np.full((1, 1, 1), 0.00), ["tile","lat", "lon"], -999.0, "kg/m2", "Intercepted liquid water stored on canopy"),
    "RHOS": create_variable(np.full((1, 1, 1), 0.00), ["tile", "lat", "lon"], -999.0, "kg/m3", "Density of snow"),
    "ROOT": create_variable(np.full((1, 4, 1, 1), -999.00), ["tile", "ic", "lat", "lon"], -999.0, "m", "Annual maximum rooting depth of vegetation category"),
    "SAND": create_variable(np.full((1, 7, 1, 1), -999.00), ["tile", "layer", "lat", "lon"], -999.0, "%", "Percentage sand content, Dai et al.,2020"),
    "SCAN": create_variable(np.full((1, 1, 1), 0.00), ["tile", "lat", "lon"], -999.0, "kg/m2", "Intercepted frozen water stored on canopy"),
    "SDEP": create_variable(np.full((1, 1, 1), 1.10), ["tile", "lat", "lon"], -999.0, "m", "Soil permeable depth, Dai et al.,2020"),
    "SNO": create_variable(np.full((1, 1, 1), 0.00), ["tile", "lat", "lon"], -999.0, "kg/m2", "Mass of snow pack"),
    "SOCI": create_variable(np.full((1, 1, 1), 13.33), ["tile", "lat", "lon"], -999, "index", "Soil colour index, Gong и др., 1999"),
    # "TAC": create_variable(np.full((1, 1, 1), 280.78), ["tile", "lat", "lon"], -999.0, "K", "Temperature of air in vegetation canopy Li Xiaoyan, 2020"),
    "TBAR": create_variable(np.full((1, 7, 1, 1), -999.00), ["tile", "layer", "lat", "lon"], -999.0, "K", "Temperature of soil layers Li Xiaoyan, 2020"),
    "TCAN": create_variable(np.full((1, 1, 1), -15.47502294), ["tile", "lat", "lon"], -999.0, "K", "Vegetation canopy temperature"),
    "THIC": create_variable(np.full((1, 7, 1, 1), -999.00), ["tile", "layer", "lat", "lon"], -999.0, "m3/m3", "Volumetric frozen water content of soil layers"),
    "THLQ": create_variable(np.full((1, 7, 1, 1), -999.00), ["tile", "layer", "lat", "lon"], -999.0, "m3/m3", "Volumetric liquid water content of soil layers Li Xiaoyan, 2020"),
    "TPND": create_variable(np.full((1, 1, 1), 0.00), ["tile", "lat", "lon"], -999.0, "K", "Temperature of ponded water"),
    # "TSFS": create_variable(np.full((1, 1, 1), -15.47502294), ["tile", "lat", "lon"], -999.0, "K", "Ground surface temperature over subarea, Li Xiaoyan, 2020"),
    "TSNO": create_variable(np.full((1, 1, 1), 0.00), ["tile", "lat", "lon"], -999.0, "K", "Snowpack temperature"),
    "WSNO": create_variable(np.full((1, 1, 1), 0.00), ["tile", "lat", "lon"], -999.0, "kg/m2", "Liquid water mass in snowpack"),
    "ZPND": create_variable(np.full((1, 1, 1), 0.00), ["tile", "lat", "lon"], -999.0, "m", "Depth of ponded water on surface"),
    # "ic": create_variable(np.full((4,), np.nan), ["ic"], np.nan, "-", "CLASS PFTs (needleleaved tree, broadleaved tree, crops, grass)"),
    # "icp1": create_variable(np.full((5,), np.nan), ["icp1"], np.nan, "-", "CLASS PFTs + bareground"),
    "ipeatland": create_variable(np.full((1, 1, 1), 0.00), ["tile", "lat", "lon"], -999.0, "-", "Peatland flag: 0 = not a peatland, 1= bog, 2 = fen"),
    # "lat": create_variable(np.full((1,), np.nan), ["lat"], np.nan, "degrees_north", "latitude", standard_name="latitude", axis="Y"),
    # "layer": create_variable(np.full((8,), np.nan), ["layer"], np.nan, "-", "ground column layers"),
    # "lon": create_variable(np.full((1,), np.nan), ["lon"], np.nan, "degrees_east", "longitude", standard_name="longitude", axis="X"),
    "nmtest": create_variable(np.full((1, 1), 1.00), ["lat", "lon"], -999, "-", "Number of tiles in each grid cell"),
    # "tile": create_variable(np.full((1,), np.nan), ["tile"], np.nan, "-", "tiles", axis="Z"),
    "maxAnnualActLyr": create_variable(np.full((1, 1, 1), 12.00), ["tile", "lat", "lon"], -999.0, "m", "!< Active layer thickness maximum over the e-folding period specified by parameter eftime")
}

# Manually setting the specific values for variables with different values on different layers
variables["CLAY"][0, 0:6, 0, 0] = [0.02, 0.06, 0.07, 0.11, 0.10, 0.0946]
variables["DELZ"][0:7] = [0.1, 0.1, 0.1, 0.1, 0.1, 0.6, 0.8]
variables["ORGM"][0, 0:6, 0, 0] = [0.19, 0.07, 0.04, 0.02, 0.005923, 0.00005]
variables["SAND"][0, 0:7, 0, 0] = [0.52, 0.42, 0.39, 0.35, 0.41, 0.4237, -3]
variables["TBAR"][0, 0:7, 0, 0] = [-11.43, -9.62, -7.97, -7.38, -6.49, -2.31, -0.31]
variables["THLQ"][0, 0:7, 0, 0] = [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]
variables["THIC"][0, 0:7, 0, 0] = [0.0476, 0.056, 0.0553, 0.0502, 0.0564, 0.1168, 0.4229]
variables["ALIC"][0, 3, 0, 0] = 0.31
variables["ALVC"][0, 3, 0, 0] = 0.05
variables["CMAS"][0, 3, 0, 0] = 3
variables["FCAN"][0, 3, 0, 0] = 1
variables["LNZ0"][0, 3, 0, 0] = -3.91
variables["PAMN"][0, 3, 0, 0] = 3
variables["PAMX"][0, 3, 0, 0] = 3
variables["ROOT"][0, 3, 0, 0] = 0.4


# Adding the variables to the dataset
for var_name, var_data in variables.items():
    ds[var_name] = var_data

# Define the output file path
output_file_path = 'CLASSIC/inputFiles/Qinghai_Lake/init_file.nc'

# Write the dataset to the NetCDF file
ds.to_netcdf(output_file_path)