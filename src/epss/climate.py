"""Climate data: unit conversions and catchment-average series from ERA5-Land NetCDF."""
from pathlib import Path
import tempfile
import zipfile

import numpy as np
import pandas as pd
import xarray as xr


def _open_dataset(path):
    """Open a NetCDF file, including the zip archive format used by the course data."""
    path = Path(path)
    if zipfile.is_zipfile(path):
        members = sorted(
            name for name in zipfile.ZipFile(path).namelist() if name.lower().endswith(".nc")
        )
        if not members:
            raise ValueError(f"No NetCDF files found in archive: {path}")
        tmpdir = tempfile.mkdtemp(prefix="epss_")
        with zipfile.ZipFile(path) as zf:
            zf.extract(members[0], tmpdir)
        extracted_path = Path(tmpdir) / Path(members[0]).name
        return xr.open_dataset(extracted_path)
    return xr.open_dataset(path)


def kelvin_to_celsius(t):
    """Temperature in K -> °C."""
    out = np.asarray(t) - 273.15
    if isinstance(t, pd.Series):
        return pd.Series(out, index=t.index, name=t.name)
    return out


def to_monthly_mm(tp):
    """ERA5-Land monthly-mean precipitation (m/day) -> monthly total (mm/month).

    tp: pd.Series with a monthly DatetimeIndex (month start).
    """
    if isinstance(tp, pd.Series):
        out = tp * 1000.0 * tp.index.days_in_month.astype(float)
        out.name = tp.name
        return out
    return np.asarray(tp) * 1000.0


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
    ds = _open_dataset(nc_file)
    mr = to_meteoraster(ds[variable], variable)
    agg, _ = mr.get_values_from_KML(str(kml))
    return pd.Series(agg.iloc[:, 0].values, index=pd.DatetimeIndex(mr.production_datetime), name=variable)