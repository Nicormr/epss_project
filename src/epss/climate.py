"""Climate data: unit conversions and catchment-average series from ERA5-Land NetCDF."""
import numpy as np
import pandas as pd
import xarray as xr


def kelvin_to_celsius(t):
    """Temperature in K -> °C."""
    # TODO: Convert the temperature from kelvin to degrees Celsius.
    # In: t in K (number, array or pd.Series)
    # Out: t in °C, same type
    raise NotImplementedError('Convert the temperature from kelvin to degrees Celsius.')


def to_monthly_mm(tp):
    """ERA5-Land monthly-mean precipitation (m/day) -> monthly total (mm/month).

    tp: pd.Series with a monthly DatetimeIndex (month start).
    """
    # TODO: Convert precipitation from mean daily rate (m/day) to monthly total (mm/month): x 1000 and
    #       x days in each month (tp.index.days_in_month).
    # In: tp (pd.Series, m/day, monthly DatetimeIndex)
    # Out: pd.Series in mm/month, same index
    raise NotImplementedError('Convert precipitation from mean daily rate (m/day) to monthly total (mm/month): x 1000 and x days in each month (tp.index.days_in_month).')


def to_meteoraster(da, variable="unknown", units="unknown"):
    """xarray DataArray (valid_time, latitude, longitude) -> meteoraster.MeteoRaster.

    meteoraster's own ERA5-Land reader only reads GRIB, so the NetCDF grid is passed directly.
    """
    from meteoraster import MeteoRaster

    da = da.load()
    return MeteoRaster(
        dict(data=da.values[:, None, None, :, :].astype(float),   # [time, member, leadtime, lat, lon]
             latitudes=da["latitude"].values,
             longitudes=da["longitude"].values,
             production_datetime=pd.DatetimeIndex(da["valid_time"].values),
             leadtimes=np.array([pd.DateOffset(months=0)])),             # monthly data, no lead time
        variable=variable, units=units, verbose=False)


def catchment_polygon(kml):
    """Catchment polygon(s) from a KML file, as a list of shapely geometries (lon, lat)."""
    import shapely
    from meteoraster.zonal import read_kml_polygons

    return [shapely.from_wkt(g.ExportToWkt()) for _, g in read_kml_polygons(str(kml))]


def catchment_series(nc_file, kml, variable):
    """Area-weighted mean of a NetCDF variable over the KML polygon (original units).

    Returns a pd.Series indexed by month start.
    """
    mr = to_meteoraster(xr.open_dataset(nc_file)[variable], variable)
    agg, _ = mr.get_values_from_KML(str(kml))
    return pd.Series(agg.iloc[:, 0].values, index=pd.DatetimeIndex(mr.production_datetime), name=variable)
