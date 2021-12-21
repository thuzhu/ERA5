import geopandas as gpd
import numpy as np
import pandas as pd
import rasterstats as rstats
import netCDF4 as nc
from affine import Affine
import os

DATA_PATH = 'Data'


def main():
    # Read the national boundary
    shp_df = gpd.read_file(r'World_Map/World_Map.shp')
    # Define the projection of nc file
    affine = Affine.translation(-180.0, 90.0) * Affine.scale(0.25, -0.25)

    result = shp_df[shp_df.columns[:3]]

    for file in os.listdir(DATA_PATH):
        filename = os.path.join(DATA_PATH, file)
        rs = calculate_daily_mean(filename)
        if type(rs) is np.ndarray:
            tmp_df = zonal_statistics(shp_df, affine, rs)
            tmp_df.columns = ['%s' % filename.split('.')[0].split('_')[1]]
            result = pd.concat([result, tmp_df], axis=1).dropna(how='any')

    result.to_csv('t2m.csv', index=False, float_format='%.3f')


def calculate_daily_mean(filename):

    # Read the NetCDF file
    nc_file = nc.Dataset(filename)['t2m']
    if nc_file.__len__() == 24:
        rs = nc_file[0].data
        for i in range(1, 24):
            tmp = nc_file[i].data
            rs = (rs + tmp) / 2

        # Convert from Kelvins Degree to Celsius Degree
        rs = rs - 273.15

        return rs
    else:
        print('no sufficient value of %s' % filename)
        return 0


def zonal_statistics(shp_df, affine, rs):
    # Zonal statistics to extract national total
    result = pd.DataFrame(rstats.zonal_stats(shp_df.geometry, rs, affine=affine, stats="mean"))

    return result


if __name__ == '__main__':
    main()